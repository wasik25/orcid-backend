
BDE = 'BDE'
slant = '/'

def check_code_length(data):

	if data and len(data) >= 5:
		return True
	return False

def code_format(raw_data):

	if check_code_length(raw_data):
		if not raw_data.startswith('BDE'):
			grab_list = list(raw_data.strip().upper())
			join_data_bde = list(BDE) + grab_list
			data_list_1 = join_data_bde[0:3] + list(slant)
			data_list_2 = join_data_bde[3:5] + list(slant)
			data_list_3 = join_data_bde[5:]
			data_str = ''.join(data_list_1 + data_list_2 + data_list_3)

			return data_str

		else:
			return raw_data
	else:
		return
