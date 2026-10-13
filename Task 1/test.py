with open("Task 1/old.txt", "r") as old_file:
    old_data = [el.strip() for el in old_file.readlines()]

with open("Task 1/new.txt", "r") as new_file:
    new_data = [el.strip() for el in new_file.readlines()]

diff_data = []
idx = 0

for new_el in new_data:
    while idx < len(old_data):
        if new_el == old_data[idx]:
            diff_data.append(new_el)
            idx += 1
            break
        if new_el not in old_data[idx:]:
            diff_data.append("+" + new_el)
            break
        else:
            diff_data.append("-" + old_data[idx])
            idx += 1
    else:
        diff_data.append("+" + new_el)

with open("Task 1/diff.txt", "w") as diff_file:
    diff_file.writelines(el + "\n" for el in diff_data)
