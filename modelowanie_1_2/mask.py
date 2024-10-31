import pandas as pd
gauss = [
        [1/16, 1/8, 1/16],
        [1/8, 1/4, 1/8],
        [1/16, 1/8, 1/16]
    ]
df_gauss = pd.DataFrame(gauss)
df_gauss.to_csv('gauss.csv', sep=',', header=False, index=False)

# mask = [
#     [1/9, 1/9, 1/9],
#     [1/9, 1/9, 1/9],
#     [1/9, 1/9, 1/9]
# ]
# mask = [
#     [-1, -1, -1],
#     [-1, 9, -1],
#     [-1, -1, -1]
# ]
# górnoprzepustowy
mask =[
    [ 1, -2,  1],
    [-2,  4, -2],
    [ 1, -2,  1]
]


df = pd.DataFrame(mask)
df.to_csv('maska_staly_promien.csv', sep=',', header=False, index=False)

variable_mask = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0]
]
df_variable = pd.DataFrame(variable_mask)
df_variable.to_csv('maska_zmienny_promien.csv', sep=',', header=False, index=False)

