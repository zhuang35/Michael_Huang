import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.math.*;
import static java.lang.System.out;


public class islands {
	public static boolean is_land(char[][] map, int x, int y){
		if(map[y][x] == '-'){
			return true;
		}
		return false;
	}
	
	// recursively maps out an entire island, and on original map replaces land tiles with water
	public static void find_island (char[][] map, boolean[][] searched, int x, int y, int right, int bottom){
		searched[y][x] = true;
		if (map[y][x] != '-'){
			return;
		} else{
			map[y][x] = '#';
		}
		
		if(x > 0){
			if (!searched[y][x - 1]){
				find_island (map, searched, x - 1, y, right, bottom);
			}
		}
		if(x < right - 1){
			if (!searched[y][x + 1]){
				find_island (map, searched, x + 1, y, right, bottom);
			}
		}
		if(y > 0){
			if (!searched[y - 1][x]){
				find_island (map, searched, x, y - 1, right, bottom);
			}
		}
		if(y < bottom - 1){
			if (!searched[y + 1][x]){
				find_island (map, searched, x, y + 1, right, bottom);
			}
		}
		
		return;
	}
	
	public static int count_islands (char[][] map, int x, int y){
		int counter = 0;
		boolean[][] searched = new boolean[y][x];
		for(int i = 0; i < y; i++){
			for(int j = 0; j < x; j++){
				if(!searched[i][j]){
				if (is_land(map, j, i)){
					counter++;
					find_island(map, searched, j, i, x, y);
				}
				}
			}
		}
		
		return counter;
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
		//String file = args[0];
		String file = "testIslands.txt";
		
		try{
			BufferedReader f = new BufferedReader(new FileReader(file));
			
			int num_problems = Integer.parseInt(f.readLine());
			
			ArrayList<char[][]> problems = new ArrayList<char[][]>();
			int[][] problem_sizes = new int[num_problems][2];
			
			
			for(int p = 0; p < num_problems; p++){
				String[] yx = f.readLine().split(" ");
				int y = Integer.parseInt(yx[0]);
				int x = Integer.parseInt(yx[1]);
				problem_sizes[p][0] = y;
				problem_sizes[p][1] = x;
				
				char[][] arr = new char[y][x];
				
				for(int i = 0; i < y; i++){
					char[] temp_arr = f.readLine().toCharArray();
					for(int k = 0; k < temp_arr.length; k++){
						arr[i][k] = temp_arr[k];
					}
				}
				problems.add(arr);
				
			}
			String answer = "";
			for(int i = 0; i < num_problems; i++){
				int tx = problem_sizes[i][1];
				int ty = problem_sizes[i][0];
				answer += count_islands(problems.get(i), tx, ty) + "\n";
			}
			
			
			

			

			f.close();
			writeAnswer("testIslands_solution.txt", answer);

			
		} catch (FileNotFoundException e){
			System.out.println("File not found!");
			System.exit(1);
		} catch (IOException e){
			System.out.println("yeet");
		}
	}
}
