def ThreeMultis(lst):
	returnList = []
	if isinstance(lst, list):
		for num in lst:
			if num % 3 == 0 and num != 0:
				returnList.append(num)
	else:
		return "List input of numbers required"
		
	return returnList