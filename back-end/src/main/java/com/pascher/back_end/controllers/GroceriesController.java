package com.pascher.back_end;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import org.springframework.web.bind.annotation.CrossOrigin;

@RestController
public class GroceriesController {
    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/run-selenium-script")
    public SseEmitter runSeleniumScript() {
    SseEmitter emitter = new SseEmitter(0L); // No timeout
    ExecutorService executor = Executors.newSingleThreadExecutor();

        executor.submit(() -> {
            try {
                emitter.send("Starting Selenium script...");
                // Command to run the Python script
                ProcessBuilder processBuilder = new ProcessBuilder("python3", "/home/yan/Desktop/visual-code/pascher/scraper/scraper.py");
                processBuilder.redirectErrorStream(true);

                // Start the process
                Process process = processBuilder.start();

                // Capture the script's output and stream it line by line
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    emitter.send(line);
                }

                // Wait for the process to finish and check the exit code
                int exitCode = process.waitFor();
                if (exitCode == 0) {
                    emitter.send("Script completed successfully.");
                } else {
                    emitter.send("Script exited with code " + exitCode);
                }

                // Close the emitter after sending all data
                emitter.complete();
            } catch (Exception e) {
                try {
                    emitter.send("Error: " + e.getMessage());
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
                emitter.completeWithError(e);
            } finally {
                executor.shutdown();
            }
        });

        return emitter;
    }
}
