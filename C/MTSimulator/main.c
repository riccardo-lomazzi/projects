#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define STRTRLEN 15
#define STRINPUTLEN 2000

typedef enum
{
    false, true
} Boolean;

typedef struct
{
    char ** strings;
    int size;
} StringArray;

typedef struct
{
    int * array;
    int size;
} IntArray;

typedef struct
{
    int value;
    Boolean isFinal;
} State;

typedef struct
{
    int initial_state;
    char readC;
    char writeC;
    char move;
    int dest_state;
} Transition;

typedef struct
{
    Transition ** trArray;
    int size;
} TransitionArray;

/*TAPE DECLARATIONS*/
typedef struct node
{
    char value;
    struct node * next;
    struct node * prev;
} Cell;

typedef struct
{
    Cell * head; //not to be confused with the pointer to first element - this is the pinhead of the MT tape
    //Cell * first;
    //Cell * last;
} Tape;

typedef struct StackElement
{
    int level;
    Transition * stackTransition;
    struct StackElement * next;
} StackElement;

typedef struct
{
    int topLevel;
    StackElement * topElement;
} Stack;

typedef struct
{
    TransitionArray trArray; //transition array. Should be faster using a static variable rather than a dynamically allocated one
    IntArray asArray; //accept states array
    int current_state;
    int max_moves;
    Tape * tape;
} TuringMachine;


////MT CREATIONS
TuringMachine * createTuringMachine(FILE *); //this builds the Turing Machine by collecting data from the FILE
void readFile(FILE *, TuringMachine **, StringArray **);
//TRANSITIONS ARRAY FUNCTIONS
Transition ** readTrArray(FILE *, int *); //this builds the transitions array
Transition * createTransitionElement(char *); //creates pointer to a Transition array
void printTransition(Transition *);
void printTrArray(TransitionArray);
void freeTrArray(TransitionArray *);
//ACCEPT STATES ARRAY FUNCTIONS
int * readASArray(FILE *, int *);
void printASArray(IntArray);
//MAX MOVES FUNCTION
int readMaxMoves(FILE *);
//INPUT MANIPULATION
int stringToInt(char *);
char * my_fgets(char *, int, FILE *);
char * my_strsep(char**, const char*);
char * truncate(char *);
//MT MANIPULATION
void startMT(TuringMachine *, StringArray *, FILE *);
int searchAndPushStackConfigs(Stack **, Transition **, int, char, int);
Boolean searchAccState(IntArray *, int );
void executeTransition(TuringMachine *, Transition *);
void reverseTransition(TuringMachine *, Transition *);
void printMT(TuringMachine *);
void freeMT(TuringMachine **);
//STACK MANIPULATION
void initializeStack(Stack **);
Boolean isStackEmpty(Stack *);
void pushToStack(Stack **, Transition *, int);
void popFromStack(Stack **);
StackElement * newStackElement(Transition *, int);
void printStack(Stack *);
void freeStack(Stack **);
//TAPE MANIPULATION
void copyOnTape(Tape ** , char *); //to copy string on tape
void appendInTape(Cell **, char);
void insertStartTape(Cell **, char);
void rewindTape(Cell **);
void printTape(Cell **);
void freeTape(Cell **);
//INPUT STRINGS MANIPULATION
void readStrArray(FILE *, StringArray **);
void freeStrArray(StringArray **);
void printStrArray(StringArray *);

int main()
{
    FILE *fpIN, *fpOUT;
    TuringMachine * mt = NULL;
    StringArray * readStringsArray = NULL;
    printf("Welcome to Machine Turing Simulator\n");
    //file opening
    char inputFileName[30] = "ww.txt"; //<--- *your file path*
    fpIN = fopen(inputFileName, "r");
    if(fpIN == 0)
    {
        printf("Could not open file\n");
    }
    else
    {
        //lettura
        readFile(fpIN, &mt, &readStringsArray);
        fclose(fpIN);
        //printMT(mt);
        //printStrArray(readStringsArray); //uncomment these lines if you'd like to see the parsed file
        fpOUT = fopen("output.txt", "w");

        startMT(mt, readStringsArray, fpOUT);

        fclose(fpOUT);
        freeMT(&mt);
        freeStrArray(&readStringsArray);
    }
    return 0;
}

//function that creates a Turing Machine based on file reading
void readFile(FILE * inputFile, TuringMachine ** mt, StringArray ** stringsArray)
{
    //creates Turing Machine
    *mt = createTuringMachine(inputFile);
    //array of strings to run into the MT
    readStrArray(inputFile, stringsArray);
}

TuringMachine * createTuringMachine(FILE * inputFile)
{
    TuringMachine * mt = malloc(sizeof(TuringMachine));
    mt->trArray.size = 10;
    mt->asArray.size = 5;
    //Building transition data structure
    mt->trArray.trArray = readTrArray(inputFile, &(mt->trArray.size)); //creating transition array
    //Building accept state
    mt->asArray.array= readASArray(inputFile, &(mt->asArray.size));
    //set current state to 0
    mt->current_state = 0;
    //read max moves
    mt->max_moves = readMaxMoves(inputFile);
    //init_tape
    mt->tape = NULL;
    return mt;
}


Transition ** readTrArray(FILE * inputFile, int * size)  //returns a pointer to pointers of type Transition (because every Transition is allocated in the dynamic memory)
{
    char stop[4] = "";
    //read the total number of transitions
    fgets(stop,4,inputFile); //position the pointer after "tr"
    int i = 0; //i=trArray pointer
    Transition ** trArray = malloc((*size) * sizeof(Transition*)); //array of transitions
    char * row = malloc(STRTRLEN * sizeof(char));
    while(my_fgets(row, STRTRLEN, inputFile)!=NULL)
    {
        if(strcmp(row, "acc")==0)
        {
            trArray[i] = NULL; //fake value that tells eventual loops when to stop
            break;
        }
        /*We can't just wait for i>size, we need to already start allocate when i=size
        because malloc allocates size=10 elements, we access them from 0 to 9.
        So when reaching i=9, we need to already allocate more space, otherwise trArray[i] would just try to write on a unallocated memory location
        and not make realloc work properly
        */
        if(i>=(*size))
        {
            (*size)*=2; //size = size * 2;
            Transition ** temp = realloc(trArray, (*size) * sizeof(Transition*));
            //realloc errors try-catch
            if(temp==NULL)
                exit(-2);
            else
                trArray = temp;
        }
        //begin splitting the string in Transition elements
        trArray[i] = createTransitionElement(row);
        i++;
    }
    //at the last element, add a NULL pointer
    trArray[i] = NULL;
    free(row);
    //we'll free the trArrayLater
    return trArray;
}

//scan the transition row, splits it into substrings and stores data in a Transition variable
Transition * createTransitionElement(char * row)
{
    Transition * temp = malloc(sizeof(Transition));
    int i = 0, len = strlen(row);
    char * token;
    char ** substrings = malloc(len * sizeof(char*)); //array that stores every substring split from the original Transition string
    while((token = my_strsep(&row," "))!=NULL)
    {
        substrings[i] = malloc(STRTRLEN); //storing substring...
        strcpy(substrings[i], token);
        i++;
    }
    temp->initial_state = stringToInt(truncate(substrings[0]));
    temp->readC = substrings[1][0];
    temp->writeC = substrings[2][0];
    temp->move = substrings[3][0];
    temp->dest_state = stringToInt(truncate(substrings[4]));
    //free every substring created
    int j=0;
    for(j=0; j<i; j++)
    {
        free(substrings[j]);
    }
    free(substrings);
    return temp;
}

void printTransition(Transition * tr){
    printf("%d %c %c %c %d\n", tr->initial_state, tr->readC, tr->writeC, tr->move, tr->dest_state);
}

void printTrArray(TransitionArray trArray)
{
    int i=0;
    while(trArray.trArray[i]!=NULL)
    {
        printTransition(trArray.trArray[i]);
        i++;
    }
}

void freeTrArray(TransitionArray * trArray)
{
    int i=0;
    while((*trArray).trArray[i]!=NULL)
    {
        free((*trArray).trArray[i]); //let's free every Transition
        i++;
    }
    free((*trArray).trArray); //we also need to free the pointer to all the pointers
}


int * readASArray(FILE * inputFile, int * size)
{
    int i = 0;
    int * asArray = (int *)malloc((*size) * sizeof(int));
    char * row = (char *)malloc(STRTRLEN * sizeof(char));
    while(my_fgets(row, STRTRLEN, inputFile)!=NULL)
    {
        if(strcmp(row, "max")==0)
        {
            asArray[i] = -1; //fake value that tells eventual loops when to stop
            break;
        }
        //rewrite with if (i > size) then size *=2 and realloc
        if(i>=(*size))
        {
            (*size)*=2; //size = size * 2;
            asArray = (int *)realloc(asArray, (*size) * sizeof(int));
        }
        asArray[i] = stringToInt(row);
        i++;
    }
    free(row);
    return asArray;
}

void printASArray(IntArray asArray)
{
    int i=0;
    while(asArray.array[i]!=-1)
    {
        printf("%d\n", asArray.array[i]);
        i++;
    }
}

int readMaxMoves(FILE * inputFile)
{
    char * row = (char *)malloc(sizeof(char)*STRTRLEN);
    int maxMoves;
    while(my_fgets(row, STRTRLEN, inputFile)!=NULL)
    {
        if(strcmp(row, "run")==0)
        {
            break;
        }
        maxMoves = stringToInt(row);
    }
    free(row);
    return maxMoves;
}

/** \brief converts a string of integers by getting their numeric value (-48 to remove the ASCII encoding) and using
 * the base10 positional numeral system to convert them in actual number
 * \param str
 * \return integer contained in the string
 *
 */
//converts string to Integer base 10
int stringToInt(char * str)
{
    int len=strlen(str)-1, sum=0, i=0; //-1 in len means that the powers of 10 of a str with len=1 will start with exp=0
    while(len>=0 && str[i]!='\0')
    {
        sum += (str[i]-48)*((int)pow(10,len));
        len--;
        i++;
    }
    return sum;
}

/** \brief standard fgets that returns the string without the '\n' saved at the end
 *
 * \param string of chars to memorize the read chars in buffer
 * \param length of string
 * \param buffer
 */
char * my_fgets(char * str, int length, FILE * stream)
{
    char * result = fgets(str, length, stream);
    if(result == NULL){
        return result;
    }
    return truncate(str);
}

char* my_strsep(char** stringp, const char* delim)
{
    char* start = *stringp;
    char* p;

    p = (start != NULL) ? strpbrk(start, delim) : NULL;

    if (p == NULL)
    {
        *stringp = NULL;
    }
    else
    {
        *p = '\0';
        *stringp = p + 1;
    }

    return start;
}


char * truncate(char * str)
{
    int i=0;
    while(str[i]!='\n' && str[i]!='\0')
    {
        i++;
    }
    if(str[i]=='\n')
    {
        str[i]='\0';
    }
    return str;
}


void startMT(TuringMachine * mt, StringArray * strArray, FILE * fpout)
{
    int level, i, pushed, stacktopLevel;
    char esito;
    Stack * stack;
    StackElement * lastExecuted;
    for(i=0;strcmp(strArray->strings[i],"END")!=0;i++)
    {
        //initial declarations
        esito = '0';
        mt->current_state = 0;
        lastExecuted = NULL;
        stack = NULL;
        level = 0;
        stacktopLevel = -1;
        copyOnTape(&(mt->tape),strArray->strings[i]);//<--copy on tape
        initializeStack(&stack);
        while(esito!='1')
        {
            //search for all the possible transitions saved in the array, from the current state with the currently pointed char on the tape head
            pushed = searchAndPushStackConfigs(&stack, (mt->trArray.trArray), mt->current_state, mt->tape->head->value, level);

            if(isStackEmpty(stack)==true && pushed==0){ //if the stack is already empty, and the search failed, than it means that no transition was found
                break;
            }
            /*at this point, all possible transitions from the current state have been stacked.
            the execution happens only is the branch level of the computation tree hasn't exceeded the number of possible moves,
            meaning that the MT has possibly reached a loop. In that case, the "else" case shall revert the tape changes*/
            if(level < mt->max_moves && lastExecuted!=(stack->topElement)) //execute last stack entry
            {
                //if I'm going into an acceptance state, break out of the loop and accept the string
                if(searchAccState(&(mt->asArray),stack->topElement->stackTransition->dest_state) == true)
                {
                    esito = '1';
                    break;
                }
                //if the transition is executed, then the dest_state wasn't an acceptance state
                executeTransition(mt, stack->topElement->stackTransition);
                lastExecuted = stack->topElement; //save the last executed transition
            }
            else
            {
                //POP
                //last possible computation because max_moves has been reached OR we're just executing the same last transition
                if(esito != 'U' && level>=mt->max_moves){ //if we're here because the number of max moves has been reached, flag it with esito="U"
                    esito = 'U';
                }
                stacktopLevel = (stack)->topElement->level+1; //this is to avoid jumping into the first if and break immediately
                //in any case, continue popping from stack and reverting transitions
                while(isStackEmpty(stack)==false)
                {
                    if(stacktopLevel!=((stack->topElement->level)+1) && level<(mt->max_moves))
                    {
                        //if by reverting, we came back on the stack to a brother of an older tree node, let us execute it and start a new path
                        //but first, let's check if it's going to an acceptance state.
                        if(searchAccState(&(mt->asArray),stack->topElement->stackTransition->dest_state) == true)
                        {
                            printf("Acceptance state %d reached! Current state: %d \n", stack->topElement->stackTransition->dest_state, mt->current_state);
                            esito = '1';
                            break;
                        }
                        executeTransition(mt, stack->topElement->stackTransition);
                        lastExecuted = stack->topElement; //save the last executed transition
                        break;
                    }

                    stacktopLevel = stack->topElement->level;
                    //REVERSE
                    //create the reversed transition
                    Transition reversed;
                    reversed.dest_state = stack->topElement->stackTransition->initial_state;
                    reversed.writeC = stack->topElement->stackTransition->readC;
                    reversed.move = 'S';
                    if(stack->topElement->stackTransition->move == 'L')
                        reversed.move = 'R';
                    else
                    {
                        if(stack->topElement->stackTransition->move == 'R')
                        reversed.move = 'L';
                    }
                    //execute it
                    reverseTransition(mt,&reversed);
                    level--;
                    popFromStack(&stack);
                    lastExecuted = stack->topElement; //update last executed index
                }
                //after all these pops, level will be set one further than the topElement one
                if(isStackEmpty(stack)==true)
                {
                    break;
                }
            }
            level = stack->topElement->level + 1;
        }
        //write on file
        printf("Esito: %c\n", esito);
        fprintf(fpout, "%c\n", esito);
        freeStack(&stack);
        freeTape(&(mt->tape->head));
    }
}

int searchAndPushStackConfigs(Stack ** stack, Transition ** trArray, int initial_state, char charToSearch, int level){
    int i=0, pushed = 0;
    while(trArray[i]!=NULL){
        if(trArray[i]->initial_state == initial_state && trArray[i]->readC==charToSearch){
           pushToStack(stack, trArray[i], level);
           pushed++;
        }
        i++;
    }
    return pushed;
}


Boolean searchAccState(IntArray * asArray, int state)
{
    int i=0;
    while(asArray->array[i]!=-1)
    {
        if(asArray->array[i] == state)
            return true;
        i++;
    }
    return false;
}

void executeTransition(TuringMachine * mt, Transition * tr){
    mt->current_state = tr->dest_state;
    //writing on tape
    mt->tape->head->value = tr->writeC;
    Cell * currentNode = mt->tape->head;
    char move = tr->move;

    switch(move)
    {
        case 'L':
            if(mt->tape->head->prev == NULL) //if we moved to the left and there's nothing, it means it's a blank cell, and we need a blank to insert on top
                insertStartTape(&(mt->tape->head), '_');
            mt->tape->head = currentNode->prev;
            break;
        case 'R':
            if(mt->tape->head->next == NULL) //otherwise we just moved to the right
                appendInTape(&(mt->tape->head), '_');
            mt->tape->head = currentNode->next;
            break;
    }

}

void reverseTransition(TuringMachine * mt, Transition * tr){
    Cell * currentNode = mt->tape->head;
    char move = tr->move;
    mt->current_state = tr->dest_state;
    switch(move)
    {
        case 'L':
            if(mt->tape->head->prev == NULL) //if we moved to the left and there's nothing, it means it's a blank cell, and we need a blank to insert on top
                insertStartTape(&(mt->tape->head), '_');
            mt->tape->head = currentNode->prev;
            break;
        case 'R':
            if(mt->tape->head->next == NULL) //otherwise we just moved to the right
                appendInTape(&(mt->tape->head), '_');
            mt->tape->head = currentNode->next;
            break;
    }

    //writing on tape
    if(mt->tape->head == NULL){
        printf("HEAD NULL");
    }
    mt->tape->head->value = tr->writeC;
}

void printMT(TuringMachine * mt)
{
    printf("tr\n");
    printTrArray(mt->trArray);
    printf("acc\n");
    printASArray(mt->asArray);
    printf("max\n");
    printf("%d\n", mt->max_moves);
}

void freeMT(TuringMachine ** mt)
{
    freeTrArray(&((*mt)->trArray));
    free((*mt)->asArray.array);
    free((*mt)->tape);
    free(*mt);
}




//STACK MANIPULATION
void initializeStack(Stack ** stack){
    if((*stack)!=NULL){
        freeStack(stack);
    }

    *stack = malloc(sizeof(Stack));
    (*stack)->topElement = NULL;
    (*stack)->topLevel = 0;
}

Boolean isStackEmpty(Stack * stack){
    if(stack->topLevel==0 && stack->topElement == NULL)
        return true;
    return false;
}

void pushToStack(Stack ** stack, Transition * stackTransition, int level){
    StackElement * el = newStackElement(stackTransition, level);
    el->next =(*stack)->topElement;
    (*stack)->topElement = el;
    ((*stack)->topLevel)++;
}

StackElement * newStackElement(Transition * stackTransition, int level){
    StackElement * newElement = malloc(sizeof(StackElement));
    newElement->level = level;
    newElement->stackTransition = stackTransition;
    newElement->next = NULL;
    return newElement;
}

void popFromStack(Stack ** stack){
    if(isStackEmpty(*stack)==true){
        return;
    }
    StackElement * temp = (*stack)->topElement;
    (*stack)->topElement = ((*stack)->topElement)->next;
    ((*stack)->topLevel)--;
    free(temp);
}

void printStack(Stack * stack){
    if(isStackEmpty(stack)==true){
        return;
    }
    StackElement * temp = stack->topElement;
    while(temp!=NULL){
        printTransition(temp->stackTransition);
        temp = temp->next;
    }
}

void freeStack(Stack ** stack){
    while(isStackEmpty(*stack)==false){
        popFromStack(stack);
    }
    free(*stack);
}

//TAPE MANIPULATION
void copyOnTape(Tape ** tape, char * str)
{
    if(*tape == NULL){
        *tape = malloc(sizeof(Tape));
        (*tape)->head = NULL;
    }
    else
    {
        freeTape(&((*tape)->head));
    }
    int i=0;
    while(str[i]!='\0')
    {
        appendInTape(&((*tape)->head), str[i]);
        i++;
    }
    //(*tape)->first = (*tape)->head;
}

void appendInTape(Cell ** head, char element)
{
    Cell * newElement = malloc(sizeof(Cell));
    Cell * temp = *head;
    newElement->value = element;
    newElement->next = NULL;
    if(*head==NULL) //empty list
    {
        newElement->prev = NULL;
        *head = newElement;
        return;
    }


    while(temp->next!=NULL) //arrive to last element
    {
        temp = temp->next;
    }

    newElement->prev = temp;
    temp->next = newElement;
}

void insertStartTape(Cell ** head, char element){
    Cell * newElement = malloc(sizeof(Cell));
    Cell * temp = *head;
    newElement->value = element;
    newElement->prev = NULL;
    if(*head == NULL){ //empty list
        newElement->next = NULL;
        *head = newElement;
        return;
    }

    while(temp->prev!=NULL){
        temp = temp->prev;
    }
    newElement->next = temp;
    temp->prev = newElement;
}

void rewindTape(Cell ** head)
{
    if(*head==NULL){
        return;
    }
    while((*head)->prev!=NULL){
        (*head) = (*head)->prev;
    }
}

void printTape(Cell ** head){
    if(*head==NULL){
        return;
    }
    Cell * temp = *head;
    //rewind the tape
    while(temp->prev!=NULL){
        temp = temp->prev;
    }
    //print
    while(temp!=NULL){
        printf("%c", temp->value);
        temp = temp->next;
    }
}

void freeTape(Cell ** head)
{
    if(*head==NULL)
    {
        return;
    }
    rewindTape(head);
    Cell * temp = *head;
    while(temp!=NULL)
    {
        Cell * save = temp;
        temp=temp->next;
        free(save);
    }
    *head = NULL;
}

//INPUT STRINGS MANIPULATION
void readStrArray(FILE * inputFile, StringArray ** stringArray)
{
    int i=0;
    if(*stringArray == NULL)
    {
        *stringArray = malloc(sizeof(StringArray));
        (*stringArray)->size = 10; //let's load 10 strings first
        (*stringArray)->strings = malloc(sizeof(char*)*((*stringArray)->size)); //and allocate an array of 20 strings
    }
    char * row = (char *)malloc(STRINPUTLEN * sizeof(char)); //this is the test test string that it's going to be read
    while(my_fgets(row, STRINPUTLEN-1, inputFile)!=NULL){

        if(i>=(*stringArray)->size){
            (*stringArray)->size*=2;
            (*stringArray)->strings = realloc((*stringArray)->strings, sizeof(char **)*((*stringArray)->size));
        }

        (*stringArray)->strings[i] = malloc(sizeof(char *) * strlen(row));
        strcpy((*stringArray)->strings[i], row); //copy the string in the array
        i++;
    }
    if(i<(*stringArray)->size)
    {
        (*stringArray)->strings[i] = malloc(sizeof(char *) * 4);
        strcpy((*stringArray)->strings[i], "END");
    }
    free(row);
}

void freeStrArray(StringArray ** stringArray)
{
    int i=0;
    while(strcmp((*stringArray)->strings[i],"END")!=0){
        free((*stringArray)->strings[i]);
        i++;
    }
    free((*stringArray)->strings[i]); //<-- valgrind doesn't matter
    free((*stringArray)->strings); //<-- IMPORTANT! DO NOT REMOVE!
    free(*stringArray);
}

void printStrArray(StringArray * stringArray){
    int i=0;
    while(strcmp((stringArray->strings[i]),"END")!=0){
        puts(stringArray->strings[i]);
        i++;
    }
}
