import json
import logging
import sys
from z3 import z3

from teether.constraints import check_model_and_resolve
from teether.evm.exceptions import IntractablePath
from teether.evm.state import LazySubstituteState, SymRead
from teether.project import Project
from teether.util.z3_extra_util import concrete

def set_balance(addr, bal, i_r):
    calldata = z3.Array('CALLDATA_%d' % i_r.xid, z3.BitVecSort(256), z3.BitVecSort(8))
    new_calldata = z3.Store(z3.Store(z3.Store(z3.Store(calldata, 0, 0x70), 1, 0xa0), 2, 0x82), 3, 0x31)
    for num, byte in enumerate(addr.to_bytes(32, 'big'), 4):
        new_calldata = z3.Store(new_calldata, num, byte)
    subst = [(calldata, new_calldata)]
    state = LazySubstituteState(i_r.state, subst)
    constraints = [z3.substitute(c, subst) for c in i_r.constraints]
    sha_constraints = {sha: z3.simplify(z3.substitute(sha_value, subst)) if not isinstance(sha_value, SymRead)
    else sha_value for sha, sha_value in i_r.sha_constraints.items()}
    mstart, msz = state.stack[-1], state.stack[-2]
    mm = i_r.state.memory.read(mstart, msz)
    if not isinstance(mm, SymRead):
        if all(concrete(m) for m in mm):
            return None
        mm = z3.simplify(z3.Concat([m if not concrete(m) else z3.BitVecVal(m, 8) for m in mm]))
    extra_constraints = [mm == bal]
    try:
        model = check_model_and_resolve(constraints + extra_constraints, sha_constraints)
        sloads = []
        storage = None
        for v in model:
            if v.name().startswith("SLOAD"):
                sloads.append(model.eval(model[v]).as_long())
            if v.name().startswith("STORAGE"):
                storage = z3.simplify(model[v])
        return {sl: model.eval(storage[sl]).as_long() for sl in sloads}
    except IntractablePath:
        return None

def main(code_path, output_file, target_addrs, target_bals):
    if code_path.endswith('.json'):
        with open(code_path, 'rb') as f:
            jd = json.load(f)
        p = Project.from_json(jd)
    else:
        with open(code_path) as infile:
            inbuffer = infile.read().rstrip()
    code = bytes.fromhex(inbuffer)
    p = Project(code)
    with open('%s.project.json' % code_path, 'w') as f:
        json.dump(p.to_json(), f)

    target_addrs = [int(addr, 16) for addr in target_addrs]
    target_bals = [int(bal) for bal in target_bals]
    storage_result = dict()

    addr, bal = target_addrs[0], target_bals[0]
    return_ins = p.cfg.filter_ins('RETURN')
    gen_constraints = p.get_constraints(return_ins)
    results = []
    for _, _, i_r in gen_constraints:
        stor = set_balance(addr, bal, i_r)
        if stor:
            storage_result.update(stor)
            results = [i_r] + results
            break
        results.append(i_r)
    else:
        logging.warning(f"Could not set balance of {hex(addr)} to {bal}")
    for addr,bal in zip(target_addrs[1:], target_bals[1:]):
        for i_r in results:
            stor = set_balance(addr, bal, i_r)
            if stor:
                storage_result.update(stor)
                break
        else:
            for _, _, i_r in gen_constraints:
                stor = set_balance(addr, bal, i_r)
                if stor:
                    storage_result.update(stor)
                    results = [i_r] + results
                    break
                results.append(i_r)
            else:
                logging.warning(f"Could not set balance of {hex(addr)} to {bal}")

    with open(output_file, 'w') as f:
        json.dump({"0x{0:0{1}X}".format(k, 64): "0x{0:0{1}x}".format(v, 64) for k, v in storage_result.items()}, f)

if __name__ == '__main__':

    if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
        print('Usage: %s <code> <output file> <target-address> <target-balance> [<target-address> <target-balance>] ...'
              % sys.argv[0], file=sys.stderr)
        exit(-1)

    code = sys.argv[1]
    output_file = sys.argv[2]
    target_addresses = sys.argv[3::2]
    target_balances = sys.argv[4::2]

    main(code, output_file, target_addresses, target_balances)