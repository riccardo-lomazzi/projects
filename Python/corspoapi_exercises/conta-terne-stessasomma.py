# psuedocodice
# in input passo già la prima somma 
# check(B, T):
# 	if(|B| % 3):
# 		ordina B
# 		i=1
# 		j=i+1
# 		k = n
# 		while(j<k):
# 			sum = B[i] + B[j] + B[k]
# 			if(sum = T):
# 				rimuovi B[i],B[j],B[k]
# 				if(check(B,T)):
# 					return true
# 			else:
# 				if(sum > T): #indice k troppo grande
# 					k--
# 				else: #indice j troppo piccolo
# 					j++  
# 		if(|B| = 0): #ho eliminato tutte le terne di somma T
# 			return true
# 		else
# 			return false

