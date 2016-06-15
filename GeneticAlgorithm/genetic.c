/* Edward Nusinovich */
/* Implementing Genetic Algorithm for simple functions */

#include "genetic.h"

int main(){
	
	/* SETUP AND INITIAL CONDITIONS */
	
	int popsize = 20; /* Members of the initial population (if odd, change loop iterations) */
	double *pGen = malloc(sizeof(double)*popsize); /* Leaves space for twenty doubles (160 bytes) */
	randomgen(pGen,popsize); /* Establishes first generation */
	int tolerance = 100; /* We know that the actual solution here is 0, so if a selection is within 10 of zero, we can stop the algorithm */ 
	double minfitness;
	
	int best; /* Will store the result that is currently the optimal value on the list */
	
	do{ /* Continues producing new populations until a members is good enough */
	
		int iter;
		int totaliters = popsize/2; /* We must have as many reproductive cycles as popsize/2 --- each time, two offspring are generated */
	
		double *newGen = malloc(sizeof(double)*20);
	
		for(iter=0;iter<totaliters;iter++){
	
			double *newGen = malloc(sizeof(double)*popsize); /* Will hold our new generation */
			int counter = 0; /* Stores position where members of new generation will be saved */

			double *values = funcvals(pGen,popsize);

			/* At this point we have our generation -- pGen, and our set of fitness scores -- fitness */
			double *fitness = fitnessscores(pGen, values, popsize); /* Assigns a fitness score to each population member */		
			
			/* Selects two members of our population based on roulette wheel selection */
			int *pairofchromosomes = roulettewheel(fitness, popsize);

			float firstselection = pGen[pairofchromosomes[0]];
			float secondselection = pGen[pairofchromosomes[1]];
			
			
			printtable(pGen,values,fitness,popsize);
			printf("The first selection is %f and the second is %f\n",firstselection,secondselection); exit(0);/* DEBUG, CONFIRMS THAT WE ARE RANDOMLY SELECTING FROM INIT POP */
			
			/* Mutation of population */
			printf("Before mutation:\n");
			printall(pGen,popsize);
			
			mutate(pGen,0.05,popsize); /* This suggests a relatively low likelihood of mutation */
			
			printf("After mutation\n");
			printall(pGen,popsize);
			
			/* Should continue iterating until we have a full new population */
			
			
			/* .... */
			/* .... */
			/* .... */       
			/* .... */
			
			
			pGen = newGen;
			
		}
	
	}while(minfitness>=tolerance); /* cutoff condition */
	
	printf("\nThe best solution found was %f at %f.\n",minfitness, best);	/* Inform at conclusion of algorithm */
	
	return 0;
}

/* Returns an array of two distinct elements that are selected based on fitness */
int *roulettewheel(double *fitness, int nums){

	double totalfitness = baselined(fitness,nums); 
	double *wheel = probability(fitness,totalfitness,nums); /* stores likelihood of the selection of any element [0,1) */
	
	int selected = rouletteindex(wheel, randomfloat(), nums); /* This is the index of the selected member */
	
	int secondselection; /* Next selection shouldn't be the same as the first */
	while((secondselection=rouletteindex(wheel,randomfloat(), nums))==selected){printf("Collision... Trying again...\n");} 
		
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

/* Will return a fitness score for each person (distance from max in generation) */
double *fitnessscores(double *pGen, double *values, int nums){
	
	double *fitness = malloc(sizeof(double)*nums);
	double max = maxoflist(values,nums);
	
	int i;
	for(i=0;i<nums;i++){
		fitness[i] = max - values[i]; 
	}

	return fitness;
}

double *funcvals(double *pGen, int nums){

	double *values = malloc(sizeof(double)*nums); /* Will store a fitness score for each point */

	int i;
	for(i=0;i<nums;i++){
		values[i] = objective(pGen[i]);
	}

	return values;
	}

/* (Fitness Function) x^2 will be our fitness function for first GA */
double objective(double x){
	return x*x;
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


/* Traverses each member of the population and sometimes randomly mutates based on rate */
void mutate(double *pGen, double rate, int nums){
	
	int i;
	for(i=0;i<nums;i++){
		
		float willmutate = randomfloat(); /* Condition for mutation */
		
		if(willmutate<rate)
			pGen[i]*=(willmutate*rand()/(RAND_MAX/2)); /* We are randomly generating another number in range */
	}
}




	
