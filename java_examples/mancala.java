import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.math.*;
import static java.lang.System.out;

public class mancala {
	
	static int compute_triplet(int[] set, int start){
		int l = set[start];
		int m = set[start + 1];
		int r = set[start + 2];
		
		if (m == 0){
			return l + r;
		}
		if (m == 1){
			if (l != r){
				return 1;
			} else{
				return m + l + r;
			}
		}		
		return 0;
	}

	static int compute_static_triplet (int[] set, int start){
		return set[start] + set[start + 1] + set[start + 2];
	}
	
	static int countpieces(int[] board){
		int counter = 0;
		for(int i = 0; i < 12; i++){
			if(board[i] == 1){
				counter++;
			}
		}
		return counter;
	}
	
	static int[] playmove (int[] board, int start){
		int[] returnboard = board.clone();
		for(int i = 0; i < 3; i++){
			if(returnboard[start + i] == 0){
				returnboard[start + i] = 1;
			} else{
				returnboard[start + i] = 0;
			}
		}
		
		return returnboard;
	}
	
	static int[] possible_moves (int[] board){
		int[] moves = new int[12];
		int[] returnboard = board.clone();
		int index = 0;
		
		for(int i = 0; i < board.length - 2; i++){
			if(compute_triplet(board, i) != compute_static_triplet(board, i)){
				moves[index] = i;
				index++;
			}
		}
		if(index == 0){
			return null;
		}
		
		int[] returnmoves = new int[index];
		System.arraycopy(moves, 0, returnmoves, 0, index);
		
		return returnmoves;
	}
	
	static int[] make_move(int[] board, int move){
		int[] returnboard = board.clone();
		board = playmove(board, move);
		
		return board;
	}
	
	static int solveset(int[] board){
		Stack<int[]> searchstack = new Stack<int[]>();
		// 
		int[] bestsetsofar = new int[12];
		int bestcount = Integer.MAX_VALUE;
		

		searchstack.push(board);
		
		while(!searchstack.isEmpty()){
			int[] currentboard = searchstack.peek();
			int[] moves = possible_moves(searchstack.pop());

			
			int pieces = countpieces(currentboard);
			
			if(pieces == 0 || pieces == 1){
				return pieces;
			}
			
			if(pieces < bestcount){
				bestcount = pieces;
			}
			
			if (moves == null){
				continue;
			}
			
			for(int i = 0; i < moves.length; i++){
				searchstack.push(make_move(currentboard, moves[i]));
			}
			
			
			
		}
		return bestcount;
	}
	
	public static void writeAnswer(String path, String line){
		BufferedReader br = null;
		File file = new File(path);

		try{
			if(!file.exists()){
				file.createNewFile();
			}
			FileWriter fw = new FileWriter(file.getAbsolutePath(), false);
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(line+"\n");;
			bw.close();

		} catch(IOException e){
			e.printStackTrace();
		} finally{
			try{
				if (br != null)br.close();
			} catch(IOException ex){
				ex.printStackTrace();
			}
		}

	}

	public static void main(String[] args){
		String file = "testMancala.txt";
		try{
			BufferedReader f = new BufferedReader(new FileReader(file));

			int num_problems = Integer.parseInt(f.readLine());
			int[][] problems = new int[num_problems][12];
			String answer = "";
			for(int i = 0; i < num_problems; i++){
				String[] temp = f.readLine().split(" ");
				
				for(int j = 0; j < 12; j++){
					problems[i][j] = Integer.parseInt(temp[j]);
				}
				answer += Integer.toString(solveset(problems[i])) + "\n";
			}

			f.close();
			writeAnswer("testMancala_solution.txt", answer);

		} catch (FileNotFoundException e){
			System.out.println("File not found!");
			System.exit(1);
		} catch (IOException e){
			System.out.println("Error");
		}
	}
}
