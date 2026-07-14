def chunk_to_value(chunk):
	total_Value = 0
	if chunk[0] == "r":
		total_Value += 4
	elif chunk[0] == "-":
		total_Value += 0
	if chunk[1] == "w":
		total_Value += 2
	elif chunk[1] == "-":
		total_Value += 0
	if chunk[2] == "x":
		total_Value += 1
	elif chunk[2] == "-":
		total_Value += 0
	return total_Value


def permission_to_octal(perm_string):
	user_chunk = perm_string[0:3]
	group_chunk = perm_string[3:6]
	other_chunk = perm_string[6:9]
	if other_chunk[1] == "w" or other_chunk[2] == "x":
                print("WARNING: OTHER GROUP HAS EXCESSIVE PERMISSIONS")
	user_value = str(chunk_to_value(user_chunk))
	group_value = str(chunk_to_value(group_chunk))
	other_value = str(chunk_to_value(other_chunk))
	final_value = user_value + group_value + other_value
	return final_value




print(permission_to_octal("rwxr-xr--"))
print(permission_to_octal("rwxr-xrwx"))
