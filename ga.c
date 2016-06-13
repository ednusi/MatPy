/* Edward Nusinovich */
/* Implementing GA */

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int main(){

	float *pGen = malloc(sizeof(int)*20);

	srand(time(NULL));

	int i;
	for(i=0;i<20;i++){
		pGen[i]=rand()/(i+1);
		printf("%d\n",pGen[i]);
	}


}

/* (Fitness Function) This returns the value of 1/x^2 or -1, which is if x is 0*/
float invsquare(float x){

	return x==0 ? -1: 1/(x*x);

}


	
