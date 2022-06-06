import hashlib as hl

concat_list = [0 for i in range(100)]
current_hash = [0 for i in range(100)]
usr_count=0

class block:
    curr_hash=""
    prev_hash=""
    ac_name=""
    name=""
    age=0
    med_rep=""
    permitted_users=""
    
    def constructor(self, h,n,a,b,c,d):
        self.prev_hash=h
        self.ac_name=n
        self.name=a
        self.age=b
        self.med_rep=c
        self.permitted_users=d

    def mineBlock(self, in_str, diff_level):
        '''
        Mines the block using the input data string.
        Puzzle difficulty level is set.
        Puzzle is solved.
        Hashed string is returned.
        '''
        print("In mine: ")
        nonce = 0
        src_str=in_str
        src_str+=str(nonce)
        src_str=(hl.sha256(src_str.encode())).hexdigest()
        tgt=""
        for i in range(diff_level):
            tgt+=str(0)
            
        while (src_str[:diff_level] != tgt):
            src_str=in_str
            nonce+=1
            src_str+=str(nonce)
            print("Mining: ", nonce)
            src_str=(hl.sha256(src_str.encode())).hexdigest()
        print("Key (nonce value): ", nonce)
        print("Block mined successfully! \n")
        return src_str

    def verify_transaction(self,enc_int,ver_in,p,r):
        print("Transaction Verification in Progress: ")
        gen_prime=generator(p)
        b=1
        h,val1,val2=1,1,1
        usr_b = ver_in
        s=(r+ver_in*enc_int)%(p-1)

        for k in range(enc_int):
            b=b*gen_prime
            b%=p
            print("[---|---]")

        for k in range(r):
            h*=gen_prime
            h%=p

        for i in range(s):
            val1*=gen_prime
            val1%=p

        val2 = (h*(pow(b,usr_b)))%p
        
        if (val1==val2):
            return True
        else:
            return False

def gcd(r,p,k):
    g=1
    for x in range(k+1):
        g*=r
        g%=p
        print("Inside gcd()",g,"\n")
    return g

def generator(p):
    for i in range(2,int(p)):
        k=0
        random=[]
                
        while(True):
            num=gcd(i,p,k)
            #print(random)
            if len(random)==(p-1):                
                #print(i)
                return i
            if(num in random):
                random.clear()
                break
            else:
                random.append(num)
                k+=1  

def authenticate_key(obj, key):
    key_flag=False
    for k in range(usr_count):
        det_str=concat_list[k]+str(key)
        
        if((hl.sha256(det_str.encode())).hexdigest()==current_hash[k]):
            hash_match_index=k
            key_flag=True
            break
    
    for l in range(usr_count):
        if(obj[l].name==obj[hash_match_index].name):
            name_match_index=l
    
    if(hash_match_index!=name_match_index or key_flag==False):
        return False, None
    else:
        return True, hash_match_index

def name_encoder(usr_name):
    '''
    Encryptes the string into integer.
    Input: Hashed user name in hexadecimal.
    Output: n-digit integer extracted from the input.
    '''
    enc_int=""
    usr_name=(hl.sha256(usr_name.encode())).hexdigest()
    for i in range(len(usr_name)):
        if(usr_name[i] not in ['a','b','c','d','e','f']):
            enc_int+=usr_name[i]
    
    '''To choose n according to security level required to verify transaction.
    '''
    n=2
    if(len(enc_int)>n):
        return int(enc_int[:n])
    else:
        return int(enc_int)

def verifier_input():
    return int(input("This is Verifier Space!\nEnter a random bit 0 or 1\n"))

def prover_input():
    prime=int(input("This is Prover Space!\nEnter a prime number:\n"))  
    random=int(input("This is Prover Space!\nEnter a random number b/w 2 and(prime -1)\n"))

    return prime,random

def createBlock(obj):
    '''
    Takes input from input file or console.
    The block is mined.
    '''
    global usr_count
    
    f=open("input.txt","r")
    data_list=f.readlines()
    f_list=[]
    for x in data_list:
        if x!= '\n':
            f_list.append(x)
    i=usr_count
    usr_name = f_list[4*i].strip('\n')
    usr_med_rep = f_list[4*i+1].strip('\n')
    usr_permitted = f_list[4*i+2].strip('\n')
    usr_age = f_list[4*i+3].strip('\n')
    
    
 
    if (i==0):
        prev_hash="0"
    else:
        prev_hash=obj[i-1].curr_hash

    usr_name_en=(hl.sha256(usr_name.encode())).hexdigest()
    print(usr_name," : ",usr_name_en)
    
    
    obj[i].constructor(prev_hash,usr_name, usr_name_en, usr_age, usr_med_rep, usr_permitted)
    det_str=obj[i].prev_hash+obj[i].name+str(obj[i].age)+obj[i].med_rep+obj[i].permitted_users
    
    concat_list[i]=det_str
    obj[i].curr_hash=obj[i].mineBlock(det_str, 2)
    current_hash[i]=obj[i].curr_hash
    
    i+=1
    usr_count=i

def viewSelf(obj):
    key=input("Enter your key to view details:\n")
    
    key_authen,ind_match=authenticate_key(obj, key)
    if(key_authen==False):
        print("Invalid key! Please try again _/\_\n")
    else:
        print("........Data.........")
        print("Name: ", obj[ind_match].ac_name)
        print("Age: ", obj[ind_match].age)
        print("Health condition(s): ", obj[ind_match].med_rep)
        print("Permitted users: ", obj[ind_match].permitted_users)

def updateSelf(obj):
    global usr_count
    key=input("Enter your key to update:\n")
    key_authen,ind=authenticate_key(obj, key)
    if(key_authen==False):
        print("Invalid key! Please try again _/\_\n")
    else:
        usr_in=input("Update health condition(s)? (y/n)\n")
        if(usr_in=="y" or usr_in=="Y"):
            report_up=input("Enter updated health condition(s):\n")
        else:
            report_up=obj[ind].med_rep
        
        usr_in=input("Update age? (y/n)\n")
        if(usr_in=="y" or usr_in=="Y"):
            age_up=input("Enter updated age:\n")
        elif(usr_in=="n"or usr_in=="N"):
            age_up=obj[ind].age
        
        usr_in=input("Update permitted names? (y/n)\n")
        if(usr_in=="y" or usr_in=="Y"):
            permitted_names_up=input("Enter updated permissable names:\n")
        else:
            permitted_names_up=obj[ind].permitted_users
        
        i=usr_count
        prev_hash=obj[i-1].curr_hash
        
        obj[i].constructor(prev_hash, obj[ind].ac_name ,obj[ind].name, age_up, report_up, permitted_names_up)
        det_str=obj[i].prev_hash+obj[i].name+str(obj[i].age)+obj[i].med_rep+obj[i].permitted_users
        concat_list[i]=det_str
        obj[i].curr_hash=obj[i].mineBlock(det_str, 2)
        current_hash[i]=obj[i].curr_hash
        print("Details updated\n")
        i+=1
        usr_count=i

def viewOtherUser(obj):
    name_match_index=-1
    
    patient_name=input("Enter patient's encrypted name:\n")
    
    for l in range(usr_count):
        if(patient_name==obj[l].name):
            name_match_index=l
            
    if(name_match_index==-1):
        print("Invalid key! Please try again _/\_\n")
    else:
        acc_names=(obj[name_match_index].permitted_users).split(",")
        print("*Shown for testing purposes*\nPermitted names: ",acc_names)
        
        usr_name=input("Enter your name:\n")
        if usr_name not in acc_names:
            print("Sorry, your name is not in permitted list")
        else:
            print("Executing zero knowledge proof")
            en_int=name_encoder(usr_name)
            status=False
            while(status!=True):
                prime,random=prover_input()
                ver_in=verifier_input()
                status=obj[name_match_index].verify_transaction(en_int,ver_in,prime,random)
            
            if status==True:
                print("........Data.........")
                print("Name: ", obj[name_match_index].ac_name)
                print("Age: ", obj[name_match_index].age)
                print("Health condition(s): ", obj[name_match_index].med_rep)
                print("Permitted users: ", obj[name_match_index].permitted_users)
                
def main():
    obj = [block() for i in range(10)]
    exit_flag=False
    while(exit_flag!=True):
        print("Please enter among the below numbers to continue:")
        usr_in = input("1.Create profile\n2.View profile\n3.Update profile\n4.View other's profile\n0.Exit program\n")
        #print(usr_in)
        if(usr_in == '1'):
            createBlock(obj)
        elif(usr_in == '2'):
            viewSelf(obj)
        elif(usr_in == '3'):
            updateSelf(obj)
        elif(usr_in == '4'):
            viewOtherUser(obj)
        elif(usr_in=='0'):
            exit_flag=True
            #print(dir(obj[0]))
            print("Thank you for utilizing the Health Care Register\n_/\_")
        else:
            print ("Please try again with valid options :")

main()

