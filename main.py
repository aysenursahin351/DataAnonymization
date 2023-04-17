import pandas as pd
from faker import Faker
import matplotlib.pyplot as plt
import hashlib
import copy as cp
from anonympy.pandas import dfAnonymizer

print("----------------------Data Anonymizer----------------------")
print("Please write name of the dataset you want to anonymize!")

fileName = input()
df = pd.read_csv(fileName, sep=",")

print("Please choose one of the anonymization techniques below!")
print("1-)Anonymize with unique value")
print("2-)Anonymize with hash function")
print("3-)Anonymize with fake name data")
print("4-)Anonymize with noisy or rounding data")
choice = input("Your Choice: ")

def print_plot(title, xlabel, ylabel, keys, values):
    plt.bar(keys, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, size=8)
    plt.show()

if(choice == "1") :
    def anonymize_uniq_value(df, cols):
        for col_name in cols:
            keys = {cats: i for i, cats in enumerate(df[col_name].unique())}
            df[col_name] = df[col_name].apply(lambda x: keys[x])
        return df, keys

    print("Write the column names you want to anonymize in 'abc,def' format.")
    cols = input("Column names: ")
    cols = cols.split(",")
    df, keys = anonymize_uniq_value(df, cols)

    df.to_csv("anonymized_data.csv", index=False)

    key = list(keys.keys())
    uniques = list(keys.values())

    plt.bar(key, uniques)
    plt.title("Key-Value Pairs")
    plt.xlabel("Values")
    plt.ylabel("Keys")
    plt.xticks(rotation=45, size=8)
    print("The anonymization process was finished and the related graphics were printed!")
    plt.show()

elif(choice == "2") :
    print("Write the column name you want to anonymize in 'abc' format")
    col_name = input("Column name: ")

    # create the hash
    df['Hash'] = df[col_name].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:8])

    # save to a dictionary
    name_lookup = dict(zip(df['Hash'], df[col_name]))

    # now delete the "input" column
    df = df.drop([col_name], axis=1)
    df.to_csv('anonymized_data.csv', index=False)

    sub_dict = dict(list(name_lookup.items())[0: 10])
    hashs = list(sub_dict.keys())
    values = list(sub_dict.values())

    plt.bar(hashs, values)
    plt.title("Hash-Value Pairs")
    plt.xlabel("Hashs")
    plt.ylabel("Values")
    plt.xticks(rotation=45, size=8)
    plt.yticks(size=8)
    print("The anonymization process was finished and the related graphics were printed!")
    plt.show()

elif(choice == "3") :
    fake = Faker()
    def Sex(row):
        if row['Sex'] == 'female':
            new_name = fake.name_female()
        else:
            new_name = fake.name_male()
        return new_name

    backup_df = cp.deepcopy(df)
    df['Name'] = df.apply(Sex, axis=1)

    df.to_csv('anonymized_data.csv', index = False)

    big_dict = dict(zip(backup_df['Name'], df['Name']))
    sub_dict = dict(list(big_dict.items())[0: 10])
    fake_names = list(sub_dict.keys())
    real_names = list(sub_dict.values())

    plt.bar(fake_names, real_names)
    plt.title("Fake and Real Name Pairs")
    plt.xlabel("Real Names")
    plt.ylabel("Fake Names")
    plt.xticks(rotation=70, size=7)
    plt.yticks(size=8)
    print("The anonymization process was finished and the related graphics were printed!")
    plt.show()

elif(choice == "4") :
    anonym = dfAnonymizer(df)
    print("Choose one of these two techniques.")
    print("Write '1' for choosing the noisy method, '2' for choosing rounding method.")
    choice = input("Your choice: ")

    if (choice == '1') :
        print("Write the column name you want to anonymize in 'abc' format.")
        print("Make sure the column contains an integer value. ")
        col_name = input("Column name: ")
        anonym.numeric_noise(col_name)

        backup_df = cp.deepcopy(df)
        df = anonym.to_df()
        df.to_csv('anonymized_data.csv', index=False)

        big_dict = dict(zip(backup_df[col_name], df[col_name]))
        sub_dict = dict(list(big_dict.items())[0: 10])
        real_numbers = list(sub_dict.keys())
        noisy_numbers = list(sub_dict.values())
        noise_amount = [None] * 10

        for i in range(len(noisy_numbers)):
            noise_amount[i] = noisy_numbers[i] - real_numbers[i]

        # convert int list to str list for plot bar
        real_numbers = [str(x) for x in real_numbers]

        plt.bar(real_numbers, noise_amount)
        plt.title("Real Values and Noisy Amounts")
        plt.xlabel("Real Values")
        plt.ylabel("Noisy Amount")
        plt.xticks(size=8)
        print("The anonymization process was finished and the related graphics were printed!")
        plt.show()

    elif (choice == '2') :
        print("Write the column name you want to anonymize in 'abc' format.")
        print("Make sure the column contains an integer value. ")
        col_name = input("Column name: ")
        anonym.numeric_rounding(col_name, 2)

        backup_df = cp.deepcopy(df)
        df = anonym.to_df()
        df.to_csv('anonymized_data.csv', index=False)

        big_dict = dict(zip(backup_df[col_name], df[col_name]))
        sub_dict = dict(list(big_dict.items())[0: 10])
        real_numbers = list(sub_dict.keys())
        rounded_numbers = list(sub_dict.values())
        rounding_amount = [None] * 10

        for i in range(len(rounded_numbers)):
            rounding_amount[i] = rounded_numbers[i] - real_numbers[i]

        # convert int list to str list for plot bar
        real_numbers = [str(x) for x in real_numbers]

        plt.bar(real_numbers, rounding_amount)
        plt.title("Real Values and Rounding Amounts")
        plt.xlabel("Real Values")
        plt.ylabel("Rounding Amounts")
        plt.xticks(size=8)
        print("The anonymization process was finished and the related graphics were printed!")
        plt.show()



