/* Edward Nusinovich */
/* Implementing GA */


#include "genetic.h"

int main(){
	
	int popsize = 20;

	double *pGen = malloc(sizeof(double)*popsize); /* Leaves space for twenty doubles (160 bytes) */
	
	randomgen(pGen,popsize); /* Establishes first generation */
	printall(pGen,popsize);	

	double *fitness = fitnessscores(pGen,popsize); /* Assigns a fitness score to each population member */		
	printall(fitness,popsize);
	
	/* At this point we have our 1st generation -- pGen, and our first set of fitness scores -- fitness */
	int *pairofchromosomes = roulettewheel(fitness, popsize);

	printf("Our first selection was %f\nand our second selection was %d\n",pGen[pairofchromosomes[0]],pGen[pairofchromosomes[1]]);
	
	return 0;
}

/* Returns an array of two distinct elements that are selected based on fitness */
int *roulettewheel(double *fitness, int nums){

	double totalfitness = baselined(fitness,nums); 
	double *wheel = probability(fitness,totalfitness,nums); /* stores likelihood of the selection of any element [0,1) */
	
	int selected = rouletteindex(wheel, ((double)rand())/RAND_MAX, nums); /* This is the index of the selected member */
	
	int secondselection; /* Next selection shouldn't be the same as the first */
	while((secondselection=rouletteindex(wheel,((double)rand())/RAND_MAX, nums))==selected){printf("Collision... Trying again...\n");} 
		
	int *pairofchromosomes = malloc(sizeof(int)*2);
	
	printf("The probability of the first was %f, the second was %f\n", wheel[selected], wheel[secondselection]);
	
	pairofchromosomes[0] = selected;
	pairofchromosomes[1] = secondselection;
	
	return pairofchromosomes; /* Returns a pair of distinct elements */
}

/* Selects an index based on its weight */
int rouletteindex(double *wheel, double randbaselined, int nums){
	
	int i;
	for(i=0;i<nums;i++){
		if(randbaselined<wheel[i]) return i;
		randbaselined = randbaselined - wheel[i];
	}
}

/* Baselines the list of fitness scores, returns total fitness */
double baselined(double *fitness, int nums){
	
	double baseline = minoflist(fitness,nums); /* Will set the baseline to the minimum fitness score */

	double totalfitness=0;

	int i;
	for(i=0;i<nums;i++){
		fitness[i]=fitness[i]-baseline; /* Will set every point to be relative to the baseline */
		totalfitness = totalfitness + fitness[i];
	}

	return totalfitness;
}

/* Returns the probability that any individual element would be selected */
double *probability(double *fitness,double totalfitness, int nums){

	double *probability = malloc(sizeof(double)*nums);

	int i;
	for(i=0;i<nums;i++){
		probability[i] = fitness[i]/totalfitness;
	}

	return probability;
}

/* Will return a fitness score for each person */
double *fitnessscores(double *pGen, int nums){

	double *fitness = malloc(sizeof(double)*nums); /* Will store a fitness score for each point */

	int i;
	for(i=0;i<nums;i++){
		fitness[i]=negsquare(pGen[i]);
	}

	return fitness;
}

/* (Fitness Function) Negative x^2 will be our fitness function for first GA */
double negsquare(double x){
	return -x*x;
}



	
