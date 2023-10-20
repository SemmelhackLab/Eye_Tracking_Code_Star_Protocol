import glob
import pickle

# dir_name_sidecam='C:\\Users\\user\\Downloads\\PICKLE FILES (4)\\11112022_BLURVSNOBLUR\\'
dir_name_sidecam = 'C:\\Users\\user\\Downloads\\Videos_methods\\Videos_methods\\Distance_1712\\Distance_1712\\12\\Strike'
#dir_name_sidecam='C:\\Users\\user\\Downloads\\2023_04_02_PCIKLEFILES_FS\\2023_04_02_PCIKLEFILES_FS\\'
pickle_files = glob.glob(dir_name_sidecam + "\\*.pickle", recursive=True)
print(pickle_files)
list_data = []
for i in range(0, len(pickle_files)):
    with open(pickle_files[i], "rb") as f:
        print(pickle_files[i])

        #              u = pickle._Unpickler(f)
        #              u.encoding = 'latin1'
        strike_frame = pickle.load(f)
        #              mag_final= pickle.load(f)

        # if i == 0:
        #  print(strike_frame)
        #  strike_frame.pop(0)
    print(strike_frame)
    # strike_frame.append(671)
    # strike_frame.append(687)
    # strike_frame.append(718)
    # strike_frame.append(745)
    # strike_frame.append(815)
    # strike_frame.append(853)
    # print(pickle_files[i])
    #
    # with open(pickle_files[i], 'wb') as file:
    #         pickle.dump(strike_frame, file)
        #list_data.append(strike_frame)