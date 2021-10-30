

# def Re2Cl(Re):
#     '''
#     R² = 0.9996
#     '''
#     if Re>10e5:
#        Cl=1.0423
#     if 2e5<Re<10e5:
#         Cl=-(1e-7)*Re + 1.175
#     elif 1e5<Re<2e5:
#         print(Re)
#         Cl=-(4e-7)*Re + 1.236
#     elif Re<1e5:
#         print(Re)
#         Cl=(1e-5)*Re + 0.0231
#     return Cl

def Re2Cl(Re):
    Re_point=[50000,100000,200000,500000,1000000]
    alpha_point=[0.6075,1.1919,1.1478,1.11,1.0423]
    if Re<=Re_point[0]:
        alpha=alpha_point[0]
    elif Re>=Re_point[-1]:
        #alpha=(Re-Re_point[-1])/(Re_point[-1]-Re_point[-2])*(alpha_point[-1]-alpha_point[-2])+alpha_point[-2]
        alpha=alpha_point[-1]
    else:
        for i in range(1,len(Re_point)):
            if Re_point[i]>Re:
                alpha=(Re-Re_point[i-1])/(Re_point[i]-Re_point[i-1])*(alpha_point[i]-alpha_point[i-1])+alpha_point[i-1]
                break
    
    return alpha


def Re2alpha(Re):
    Re_point=[50000,100000,200000,500000,1000000]
    alpha_point=[3.5,10.25,9.5,8.75,7.75]
    if Re<=Re_point[0]:
        alpha=alpha_point[0]
    elif Re>=Re_point[-1]:
        alpha=(Re-Re_point[-1])/(Re_point[-1]-Re_point[-2])*(alpha_point[-1]-alpha_point[-2])+alpha_point[-2]
        # alpha=alpha_point[-1]
    else:
        for i in range(1,len(Re_point)):
            if Re_point[i]>Re:
                alpha=(Re-Re_point[i-1])/(Re_point[i]-Re_point[i-1])*(alpha_point[i]-alpha_point[i-1])+alpha_point[i-1]
                break
    return alpha

if __name__ == '__main__':
    Re=2000000
    print(Re2alpha(Re))
        


