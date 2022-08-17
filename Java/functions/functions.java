package functions;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;

import java.time.format.DateTimeFormatter;  
import java.time.LocalDateTime;

import java.util.List;

public class functions {
	static public String[] read(String filename) throws IOException {
		Path file = new File(filename).toPath();
		Charset charset = Charset.defaultCharset();  

		String[] lines = {};

		try {
			List<String> read_lines = Files.readAllLines(file, charset);
			lines = read_lines.toArray(new String[]{});
		}

		catch(IOException e) {
			e.printStackTrace();
		}

		return lines;
    }

	static public String[] Read_Lines(String file) {
		String[] lines = {};

		try {
			lines = read(file);
		}catch(IOException e) {}

		return lines;
	}

	static public String Now() {
		DateTimeFormatter dtf = DateTimeFormatter.ofPattern("HH:mm dd/MM/yyyy"); 
		LocalDateTime now = LocalDateTime.now();
		String now_text = now.format(dtf);

		return now_text;
	}
}