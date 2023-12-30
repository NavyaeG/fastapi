
# Initializing dictionary
test_dict = [{"Arushi": 22, "Anuradha": 21, "Mani": 21, "Haritha": 21},{"Arushi": 23, "Anuradha": 31, "Mani": 25, "Harith": 40}]

for i in range(len(test_dict)):
    if test_dict[i]["Mani"]==25:
        print(test_dict[i])
        print(i)
        test_dict.pop(i)
print(test_dict)