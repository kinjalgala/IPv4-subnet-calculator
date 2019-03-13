import random
import sys

def subnet_calc():
    try:
        print("\n")
		
        #Checking IP address validity
        while True:
            ip_address = input("Please enter an IP address that you wish to use: ")
			
            #Checking octets            
            ip_address_octets = ip_address.split('.')
       
            if (len(ip_address_octets) == 4) and (1 <= int(ip_address_octets[0]) <= 223) and (int(ip_address_octets[0]) != 127) and (int(ip_address_octets[0]) != 169 or int(ip_address_octets[1]) != 254) and (0 <= int(ip_address_octets[1]) <= 255 and 0 <= int(ip_address_octets[2]) <= 255 and 0 <= int(ip_address_octets[3]) <= 255):
                break
            
            else:
                print("\nThe IP address is INVALID! Please retry!\n")
                continue
		
        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
		
        #Checking Subnet Mask validity
        while True:
            subnet_mask = input("Please enter a subnet mask: ")
            
            #Checking octets            
            mask_octets = subnet_mask.split('.')
            
            if (len(mask_octets) == 4) and (int(mask_octets[0]) == 255) and (int(mask_octets[1]) in masks) and (int(mask_octets[2]) in masks) and (int(mask_octets[3]) in masks) and (int(mask_octets[0]) >= int(mask_octets[1]) >= int(mask_octets[2]) >= int(mask_octets[3])):
                break
            
            else:
                print("\nThe subnet mask is INVALID!\n")
                continue
         
        #Convert mask to binary string
        mask_octets_binary = []
        
        for octet in mask_octets:
            binary_octet = bin(int(octet)).lstrip('0b')
            #print(binary_octet)
            
            mask_octets_binary.append(binary_octet.zfill(8))
          
        binary_mask = "".join(mask_octets_binary)
        number_zeros = binary_mask.count("0")
        number_ones = 32 - number_zeros
        no_of_hosts = abs(2 ** number_zeros - 2) #return a positive value for the /32 mask (all 255s)
        
        #Obtaining wildcard mask
        wildcard_octets = []
        
        for octet in mask_octets:
            wild_octet = 255 - int(octet)
            wildcard_octets.append(str(wild_octet))
        wildcard_mask = ".".join(wildcard_octets)
        #Convert IP to binary string
        ip_address_octets_binary = []
        
        for octet in ip_address_octets:
            binary_octet = bin(int(octet)).lstrip('0b')
             
            ip_address_octets_binary.append(binary_octet.zfill(8))
          
        binary_ip = "".join(ip_address_octets_binary)
 
        #Getting the network address and broadcast address from the binary strings obtained above
        
        network_address_binary = binary_ip[:(number_ones)] + "0" * number_zeros
        
        broadcast_address_binary = binary_ip[:(number_ones)] + "1" * number_zeros
        
        #Converting everything back to decimal (readable format)
        net_ip_address_octets = []
        
        for bit in range(0, 32, 8):
            net_ip_octet = network_address_binary[bit: bit + 8]
            net_ip_address_octets.append(net_ip_octet)
        
        net_ip_address = []
        
        for each_octet in net_ip_address_octets:
            net_ip_address.append(str(int(each_octet, 2)))
         
        network_address = ".".join(net_ip_address)
        
        
        broadcast_ip_address_octets = []
        
        for bit in range(0, 32, 8):
            broadcast_ip_octet = broadcast_address_binary[bit: bit + 8]
            broadcast_ip_address_octets.append(broadcast_ip_octet)
        
        broadcast_ip_address = []
        
        for each_octet in broadcast_ip_address_octets:
            broadcast_ip_address.append(str(int(each_octet, 2)))
        broadcast_address = ".".join(broadcast_ip_address)
       
        #Results for selected IP/mask
        print("\nThe calculated values are\n")
        print("Network address is: %s" % network_address)
        print("Broadcast address is: %s" % broadcast_address)
        print("The number of valid hosts per subnet: %s" % no_of_hosts)
        print("The wildcard mask is: %s" % wildcard_mask)
        print("Number of mask bits is: %s" % number_ones)
        print("\n")
        
        #Generation of random IP addresses in the subnet
        while True:
            generate = input("Do you want to generate random IP address from this subnet? (y/n):")
            
            if generate == "y":
                generated_ip = []
                
                #Obtain available IP address in range, based on the difference between octets in broadcast address and network address
                for indexb, octet_broadcast in enumerate(broadcast_ip_address):
                    #print(indexb, octet_broadcast)
                    for indexn, octet_network in enumerate(net_ip_address):
                        #print(indexn, octet_network)
                        if indexb == indexn:
                            if octet_broadcast == octet_network:
                                #Add identical octets to the generated_ip list
                                generated_ip.append(octet_broadcast)
                            else:
                                #Generate random number(s) from within octet intervals and append to the list
                                generated_ip.append(str(random.randint(int(octet_network), int(octet_broadcast))))
                
                #IP address generated from the subnet pool
                
                y_iaddr = ".".join(generated_ip)
                
                print("The generated random IP address is: %s" % y_iaddr)
                print("\n")
                continue
                
            else:
                print("Ok, Thanks bye!\n")
                break
#To handle exception gracefully        
    except KeyboardInterrupt:
        print("\n\nProgram aborted by user. Exiting...\n")
        sys.exit()
        
#Calling the function
subnet_calc()