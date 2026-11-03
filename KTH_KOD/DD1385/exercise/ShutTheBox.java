import java.util.*;

public class ShutTheBox {

    public Integer[] rollDices(int numberOfDices){
	Random rand=new Random();
	Integer[] ret=new Integer[numberOfDices];
	int indx=0;
	for(int i=0; i < numberOfDices; i++,indx++)
	    ret[indx] = rand.nextInt();
	return ret;
    }


    public Integer[] getInputAndParse(){
	return null;
    }

    public boolean unfeasibleSelection(Integer[] inputList, Integer[] tiles, Integer[] dices){
	return true;
    }

    public void flippTiles(Integer[] selectedTiles, Integer[] tiles, Integer[] flippedTiles){
    }

    public boolean possible2play(Integer[] dices, Integer[] tiles){
	return true;
    }

    public void showTiles(Integer[] tiles){
    }


    public static void main(String[] args){
	ShutTheBox stb=new ShutTheBox();
	stb.rollDices(2);
    }
	
	  /*	Integer[] dices = rollDices(2);
	while (possible2play(dices,tiles)){
	    Integer[] selectedTiles = getInputAndParse();
	    while (unfeasibleSelection(selectedTiles, tiles, dices))
		selectedTiles = getInputAndParse();
	    flippTiles(selectedTiles, tiles, flippedTiles);
	    showTiles();
	    dices = rollDices(2);
	}
	if(len(tiles) == 0)
	    System.out.println("Bra du fick inge negativa poäng");
	else
	    System.out.println("Bra du fick "+ calcPoints(tiles)+ " negativa poäng");
	    
    }
    */
    
}


