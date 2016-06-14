#include <time.h>
#include <stdio.h>
#include <stdlib.h>

/* PROTOTYPES */ 
int *roulettewheel(double *fitness, int nums);
double *fitnessscores(double *pGen, int nums);
double negsquare(double x);
double *probability(double *fitness,double totalfitness,int nums);
double baselined(double *fitness, int nums);
int *swapchromosomes(int firstchrom, int secondchrom);


/* Returns largest element of a list */
double maxoflist(double *list, int nums){

	double max = list[0]; /* Initially set to first value */
	int i;
	for(i=1;i<nums;i++){
		if(list[i]>max){
			max = list[i];
		}
	}

	return max;

}

/* Returns smallest element of list, to baseline */
double minoflist(double *list, int nums){

	double min = list[0];
	int i;
	for(i=1;i<nums;i++){
		if(list[i]<min){
			min = list[i];
		}
	}

	return min;
}

void randomgen(long *pGen, int nums){
	srand(time(NULL));

	/* Generates twenty numbers, at each spot we store a different random number */
	int i;
	for(i=0;i<nums;i++){
		pGen[i] = rand();	
	}
}

/* Depending on pseudorandom distribution may not be completely evenly distributed */
int randinrange(int upperbound){	
	srand(time(NULL));
	return ((double)rand()/RAND_MAX)*(upperbound); /* Gets value from zero to one and then scales up by upper bound */
}

/* Prints all numbers */
void printall(long *pNums, int nums){
	int i;
	for(i=0;i<nums;i++){
		printf("%l\n",pNums[i]);
	}
	printf("------------------\n");
}
