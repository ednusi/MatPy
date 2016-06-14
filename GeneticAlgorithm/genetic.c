/* Edward Nusinovich */
/* Implementing Genetic Algorithm for polynomial function */


#include "genetic.h"

int main(){
	
	/* SETUP AND INITIAL CONDITIONS */
	
	int popsize = 20; /* Members of the initial population */
	double *pGen = malloc(sizeof(double)*popsize); /* Leaves space for twenty doubles (160 bytes) */
	randomgen(pGen,popsize); /* Establishes first generation */
	int tolerance = 10; /* We know that the actual solution here is 0, so if a selection is within 10 of zero, we can stop the algorithm */ 
	
	
	double *newGen = malloc(sizeof(double)*popsize); /* Will hold our new generation */
	int counter = 0; /* Stores position where members of new generation will be saved */
	
	long firstselection = 0;
	long secondselection = 0;

	/* At this point we have our generation -- pGen, and our set of fitness scores -- fitness */
	double *fitness = fitnessscores(pGen,popsize); /* Assigns a fitness score to each population member */		
	
	while(counter!=popsize-1){
		
		int *pairofchromosomes = roulettewheel(fitness, popsize);

		firstselection = pGen[pairofchromosomes[0]];
		secondselection = pGen[pairofchromosomes[1]];
		
		pairofchromosomes = swapchromosomes(firstselection,secondselection);
	
	}
	return 0;
}

/* Swaps the last 8 bits of two chromosomes (crossing-over) */
/* WORKS FOR INTS, NOT DOUBLES */
int *swapchromosomes(int firstchrom, int secondchrom){
	
	int bitshift = randinrange(7);
	
	int lasteightfirst = firstchrom & (0xff>>bitshift); /* gets last eight */
	int lasteightsecond = secondchrom & (0xff>>bitshift);
	
	firstchrom = firstchrom ^ lasteightfirst; /* zeroes out last eight */
	secondchrom = secondchrom ^ lasteightsecond;
	
	firstchrom = firstchrom | lasteightsecond; /* adds in bits from opposite solution */
	secondchrom = secondchrom |lasteightfirst;
	
	int *swappedpair = malloc(sizeof(int)*2);
	swappedpair[0] = firstchrom;
	swappedpair[1] = secondchrom;
	
	return swappedpair;
}

/* Returns an array of two distinct elements that are selected based on fitness */
int *roulettewheel(double *fitness, int nums){

	double totalfitness = baselined(fitness,nums); 
	double *wheel = probability(fitness,totalfitness,nums); /* stores likelihood of the selection of any element [0,1) */
	
	int selected = rouletteindex(wheel, ((double)rand())/RAND_MAX, nums); /* This is the index of the selected member */
	
	int secondselection; /* Next selection shouldn't be the same as the first */
	while((secondselection=rouletteindex(wheel,((double)rand())/RAND_MAX, nums))==selected){printf("Collision... Trying again...\n");} 
		
	int *pairofchromosomes = malloc(sizeof(int)*2);
		
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



	
