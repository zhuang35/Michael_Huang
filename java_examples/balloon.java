import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.math.*;
import static java.lang.System.out;

public class balloon {
	
	// comparator to sort by height
	public static Comparator<int[]> ballooncomp = new Comparator<int[]>(){
		public int compare(int first[], int second[]){
			return - first[0] + second[0];
		}
	};
	
	public static int solve_subproblem (int[] balloons){
		//System.ouxt.println(Arrays.toString(balloons));
		ArrayList<int[]> set = new ArrayList<int[]>(balloons.length);
		for(int i = 0; i < balloons.length; i++){
			int[] temp = new int[2];
			temp[0] = balloons[i];
			temp[1] = i;
			set.add(temp);
		}
		
		set.sort(ballooncomp);
		
		int counter = 0;
		while(set.size() > 0){
			int[] first = set.get(0);
			firearrow(set, first[0], first[1]);
			counter++;
		}
		
		
		
		
		/*
		for(int i = 0; i < set.size(); i++){
			System.out.println(Arrays.toString(set.get(i)));
		}
		
		System.out.println("\n\n reee \n\n");
		//firearrow(set, 5, 0);
		firearrow(set, 4, 0);
		

		for(int i = 0; i < set.size(); i++){
			System.out.println(Arrays.toString(set.get(i)));
		}
		*/
		
		return counter;
	}

	// fires arrow at set height and removes balloons from set
	static void firearrow (ArrayList<int[]> list, int height, int distance){
		for(int i = 0; i < list.size(); i++){
			int[] temp = list.get(i);
			if (height == temp[0] && distance <= temp[1]){
				list.remove(i);
				firearrow(list, height - 1, temp[1] + 1);
				return;
			}
		}
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
		
		// double time = System.nanoTime();
		
		//String file = args[0];
		String file = "testBalloons.txt";
		
		try{
			BufferedReader f = new BufferedReader(new FileReader(file));
			
			int num_problems = Integer.parseInt(f.readLine());
			int[][] subproblems = new int[num_problems][];
			int arrowsneeded = 0;
			String answer = "";
			String[] temp = f.readLine().split(" ");
			//System.out.println(Arrays.toString(temp));
			for(int i = 0; i < num_problems; i++){
				int len = Integer.parseInt(temp[i]);
				String[] tempballoons = f.readLine().split(" ");
				int[] problems = new int[len];
				for(int j = 0; j < len; j++){
					problems[j] = Integer.parseInt(tempballoons[j]);
				}
				
				arrowsneeded = solve_subproblem(problems);
				answer += Integer.toString(arrowsneeded) + "\n";
			}
			
			//System.out.println(num_problems);
			//System.out.println(Arrays.toString(problems));
			//System.out.println(Arrays.deepToString(subproblems));
			
			// System.out.println(answer);

			f.close();
			writeAnswer("testBalloons_solution.txt", answer);
			// System.out.println((System.nanoTime() - time)/ 1000000);
			// System.out.println(answer);
			
		} catch (FileNotFoundException e){
			System.out.println("File not found!");
			System.exit(1);
		} catch (IOException e){
			System.out.println("yeet");
		}
		
		
	}
}
