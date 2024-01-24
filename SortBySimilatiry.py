from skimage.metrics import structural_similarity
import cv2
import numpy as np
from pathlib import Path
import sys
import os, shutil

def comparaison(path1: Path, path2: Path) -> float:


    first = cv2.imread(str(path1))
    second = cv2.imread(str(path2))

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    if first.shape != second.shape :
        #print ("Taille différente")
        # Aspect ratio
        if first.shape[0] / first.shape[1] != second.shape[0] / second.shape[1] :
            #print ("Aspect Ratio différent!")
            return 0.0
        if first.shape[0] * first.shape[1] < second.shape[0] * second.shape[1] :
            #print ("1 plus petit")
            second_gray = cv2.resize(second_gray, (first.shape[0], first.shape[1]), interpolation=cv2.INTER_LANCZOS4 )
        else :
            #print ("2 plus petit")
            first_gray = cv2.resize(first_gray, (second.shape[0], second.shape[1]), interpolation=cv2.INTER_LANCZOS4 )

    # cv2.imshow("",first_gray)
    # cv2.waitKey()

    # cv2.imshow("",second_gray)
    # cv2.waitKey()

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    #print("Similarity Score: {:.3f}%".format(score * 100))
    #print ("Comparaison ",os.path.split(path1)[1]," <> ",os.path.split(path2)[1]," = ",score)

    return score

def explore_directory(path: Path) -> None:
    """Find images in a directory and compare them all."""
    
    files = (
        list(path.glob("*.jpg")) + 
        list(path.glob("*.jpeg")) + 
        list(path.glob("*.png"))
    )
    diff = {}
    done = []

    n=1
    for f1 in files:
        f1=str(f1)
        #print (f1)
        
        for f2 in files:
            f2=str(f2)
            
            if f1 == f2 :
                continue

            # Regarde si le fichier a déjà été traité
            try:
                p=[*done].index(f2)
                #print (f2+" deja fait en position "+str(p))
                continue
            except ValueError:  
                #print (f2+" n'existe pas encore, on le crée")
                pass
            
            score=comparaison(f1,f2)
            if score >0.75 :
                #print (n,'"'+str(f1)+'" "'+str(f2)+'"',score)

                try:
                    diff[f1] = diff[f1],f2
                except KeyError :
                    diff[f1] = f2
                done.append(f1)
                done.append(f2)
                n=n+1
                
    # print ("===>")
    # print (diff)
    print ("===>")
    
    # Supprimer l'ancien fichier fssort.ini
    fssort=os.path.join(path,'fssort.ini')
    if os.path.isfile("unwanted-file.txt"):
        os.remove(fssort)
    
    # ecrit le fichier
    with open(os.path.join(path,'fssort.ini'), 'w') as f:
        
        # print files by group
        for fa in diff.keys() :
            # ecrit la clé
            print (fa) 
            f.write(os.path.split(fa)[1]+'\n')
            
            # ecrit la ou les valeurs
            if type(diff[fa]) is str :
                print (diff[fa])
                f.write(os.path.split(diff[fa])[1]+'\n')
            else :
                for fb in diff[fa] :
                    print (fb)
                    f.write(os.path.split(fb)[1]+'\n')
                    
        print ("Fichiers uniques:") 
        for f1 in files:
            f1=str(f1)
            try:
                [*done].index(f1)
                continue
            except ValueError:  
                print (f1)
                f.write(os.path.split(f1)[1]+'\n')
                pass
    f.close()
   
    
    return 



if __name__ == "__main__":
    explore_directory(Path(sys.argv[1]))