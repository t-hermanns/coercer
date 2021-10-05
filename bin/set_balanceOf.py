'''
return_ins = p.cfg.filter_ins('RETURN')
constraints = p.get_constraints(return_ins)
for i, i_path, i_r in constraints:
	calldata = z3.Array('CALLDATA_%d' % i_r.xid, z3.BitVecSort(256), z3.BitVecSort(8))
	new_calldata = z3.Store(z3.Store(z3.Store(z3.Store(calldata, 0, 0x70), 1, 0xa0),2, 0x82), 3, 0x31)
	for x in range(4,34):
		new_calldata = z3.Store(new_calldata,x,0)
	new_calldata = z3.Store(z3.Store(new_calldata,34,0x43),35,0x21)
	subst = [(calldata, new_calldata)]
	state = LazySubstituteState(i_r.state, subst)
	constraints = [z3.substitute(c, subst) for c in i_r.constraints]
	sha_constraints = {sha: z3.simplify(z3.substitute(sha_value, subst)) if not isinstance(sha_value, SymRead)
	else sha_value for sha, sha_value in i_r.sha_constraints.items()}
	mstart, msz = state.stack[-1], state.stack[-2]
	mm = state.memory[mstart:mstart+msz]
	if all(concrete(m) for m in mm):
		continue
	mm = z3.simplify(z3.Concat([m if not concrete(m) else z3.BitVecVal(m, 8) for m in mm]))
	extra_constraints = [mm == 10000]
	try:
		model = check_model_and_resolve(constraints + extra_constraints, sha_constraints)
		for v in model:
			print(v, model[v])
			if v.name() == "STORAGE_1":
				print(z3.simplify(model[v][17]))
		break
	except IntractablePath:
		continue
else:
	logging.warning("Could not set balance of 0x4321 and target-address")
'''
