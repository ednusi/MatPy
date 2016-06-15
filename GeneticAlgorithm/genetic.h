#include <time.h>
#include <stdio.h>
#include <stdlib.h>

/* PROTOTYPES */ 
int *roulettewheel(double *fitness, int nums);
double *fitnessscores(double *pGen, double *values, int nums);
double objective(double x);
double *probability(double *fitness,double totalfitness,int nums);
double baselined(double *fitness, int nums);
int *swapchromosomes(int firstchrom, int secondchrom);
void mutate(double *pGen, double rate, int nums);
double *funcvals(double *pGen, int nums);
void printtable(double *pGen, double *values, double *fitness, int nums);

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

/* Displays all of the current information about the population */
void printtable(double *pGen, double *values, double *fitness, int nums){
	
	int i;
	for(i=0;i<nums;i++){		
		printf("The number is %f, its function value is %f, and its fitness score is %f.\n",pGen[i],values[i],fitness[i]);
	}
	
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

void randomgen(double *pGen, int nums){
	srand(time(NULL));

	/* Generates twenty numbers, at each spot we store a different random number */
	int i;
	for(i=0;i<nums;i++){
		pGen[i] = rand();	
	}
}

/* Returns a float from zero to one */
float randomfloat(){
	return ((float)rand()/RAND_MAX);
}

/* Depending on pseudorandom distribution may not be completely evenly distributed */
int randinrange(int upperbound){	
	srand(time(NULL));
	return ((double)rand()/RAND_MAX)*(upperbound); /* Gets value from zero to one and then scales up by upper bound */
}

/* Prints all numbers */
void printall(double *pNums, int nums){
	int i;
	for(i=0;i<nums;i++){
		printf("%f\n",pNums[i]);
	}
	printf("------------------\n");
}
