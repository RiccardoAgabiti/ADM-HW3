#!/bin/bash

#Questo script aggiorna la directory di github (~/Documenti/GitHub_projects/ADM-HW3)

#Si sposta nella directory di git
cd ~/Documenti/GitHub_projects/ADM-HW3

#seleziona il branch da modificare
git checkout ame

#Controlla che non ci siano aggiornamenti dal main e poi carica le modifiche fatte nello stage		
git pull origin main
git pull origin ame

git add * 

#Controlla che non siano stati eliminati dei file dalla directory		 
log=`git commit -m "aggiornato" | awk '/eliminato:/{print $2}'`

#se li trova li elimina da git		
for i in $log
	do
		git rm $i; git commit -m "aggiornato"
	
done

#aggiorna il branch 		

git push origin ame
