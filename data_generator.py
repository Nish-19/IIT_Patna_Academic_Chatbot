from random import seed
from random import randint
seed(1)

def read_file(file_path):
	with open(file_path) as f:
		lines = f.readlines()
		#lst = lines.split('\n')
		lines = [obj.strip('\n') for obj in lines if obj is not '']
		print(lines)
		return lines

def generate_random_list(lst, num):
	random_list = list()
	for _ in range(num):
		random_list.append(lst[randint(0, len(lst) - 1)])
	return random_list


if __name__ == '__main__':
	cat_path = 'category.txt'
	blood_path = 'blood_group.txt'
	board_path = 'board.txt'
	mother_tongue_path = 'mother_tongue.txt'
	name_path = 'name.txt'
	state_path = 'native_state.txt'
	roll_num_path = 'rollNUm.txt'
	cat_list = read_file(cat_path)
	blood_list = read_file(blood_path)
	board_list = read_file(board_path)
	mother_tongue_list = read_file(mother_tongue_path)
	name_list = read_file(name_path)
	state_list = read_file(state_path)
	roll_num_list = read_file(roll_num_path)
	sex_list = ['M', 'F']
	#print(len(roll_num_list))	#200
	num = len(roll_num_list)
	random_cat = generate_random_list(cat_list, num)
	random_blood = generate_random_list(blood_list, num)
	#print(random_blood)
	random_board = generate_random_list(board_list, num)
	random_mother_tongue = generate_random_list(mother_tongue_list, num)
	random_name = generate_random_list(name_list, num)
	random_state = generate_random_list(state_list, num)
	random_sex = generate_random_list(sex_list, num)

	with open('student_data.csv', 'w') as f:
		f.write("Roll Number,Name,Department,Sex,Category,Blood Group,Board,Mother Tongue,State\n")
		for i in range(num):
			f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(roll_num_list[i],random_name[i],roll_num_list[i][4:6],random_sex[i],random_cat[i],random_blood[i],random_board[i],random_mother_tongue[i],random_state[i]))
