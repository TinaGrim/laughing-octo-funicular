import javax.swing.*;
import java.awt.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Future;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.ConnectException;
import java.util.List;
import java.util.ArrayList;
import java.util.JSONArray;


public class LDPlayerGUI extends JFrame {
    private JLabel timeLabel;
    private Timer timer;
    private long startTime;
    private ExecutorService executorService;
    private JTextField textField;
    private JButton sendButton;
    private JTextArea chatArea;
    private Process phpServerProcess; // Add this to track PHP server process
    private static final String PHP_API_URL = "http://127.0.0.1:8080/chatBot.php";
    private List<String> aiResponseList = new ArrayList<>();
    private String aiResponse; 
    private List<String> messageList = new ArrayList<>();
    
    public LDPlayerGUI() {
        executorService = Executors.newCachedThreadPool();
        
        
        startPHPServer(); 
        setupGUI();
        startTimer();
    }

    private void setupGUI() {
        setTitle("Girm Prime App - Java Version");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1500, 800);
        setLocationRelativeTo(null);

        // Main layout
        setLayout(new BorderLayout());
        
        // Create main panel with dark background
        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(new Color(41, 44, 59)); // #292c3b
        
        // Left panel
        JPanel leftPanel = createLeftPanel();
        leftPanel.setPreferredSize(new Dimension(450, getHeight()));
        
        // Right panel with tabs
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setBackground(new Color(41, 44, 59));
        tabbedPane.setForeground(Color.WHITE);
        
        tabbedPane.addTab("Devices", createDevicesPanel());
        tabbedPane.addTab("Auto Post", createAutoPostPanel());
        
        mainPanel.add(leftPanel, BorderLayout.WEST);
        mainPanel.add(tabbedPane, BorderLayout.CENTER);
        
        add(mainPanel);
    }
    private JPanel createDevicesPanel() {
        JPanel devices = new JPanel();
        devices.setBackground(new Color(41, 44, 59));
        devices.setLayout(new BorderLayout());
        JLabel devicesLabel = new JLabel("Devices");
        devicesLabel.setFont(new Font("Arial", Font.BOLD, 24));
        devicesLabel.setForeground(Color.WHITE);
        devices.add(devicesLabel, BorderLayout.NORTH);

        return devices;
    }
    private JPanel createLeftPanel() {
        JPanel leftPanel = new JPanel(new BorderLayout());
        leftPanel.setBackground(new Color(41, 44, 59));
        
        // Header with timer
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.setBackground(new Color(41, 44, 59));
        
        JLabel playButton = new JLabel("PLAY");
        playButton.setFont(new Font("Arial", Font.BOLD, 24));
        playButton.setForeground(Color.GREEN);
        
        JLabel stopButton = new JLabel("STOP");
        stopButton.setFont(new Font("Arial", Font.BOLD, 24));
        stopButton.setForeground(Color.RED);
        
        timeLabel = new JLabel("00:00:00");
        timeLabel.setFont(new Font("Arial", Font.PLAIN, 50));
        timeLabel.setForeground(Color.WHITE);
        
        headerPanel.add(playButton);
        headerPanel.add(stopButton);
        headerPanel.add(timeLabel);
        
        // Bottom buttons panel
        JPanel buttonPanel = createButtonPanel();
        JPanel textPanel = textPanel();

        leftPanel.add(headerPanel, BorderLayout.NORTH);
        leftPanel.add(textPanel, BorderLayout.CENTER);
        leftPanel.add(buttonPanel, BorderLayout.SOUTH);
        
        return leftPanel;
    }
    private JPanel textPanel() {
        JPanel textPanel = new JPanel(new BorderLayout());
        textPanel.setBackground(new Color(41, 44, 59));

        chatArea = new JTextArea(20,50);
        chatArea.setEditable(false);
        chatArea.setBackground(new Color(30, 30, 30));
        chatArea.setForeground(Color.WHITE);
        chatArea.setFont(new Font("Arial", Font.PLAIN, 14));
        
        // Enable text wrapping
        chatArea.setLineWrap(true);                // Enable line wrapping
        chatArea.setWrapStyleWord(true);           // Wrap at word boundaries, not character boundaries
        
        // Add scroll pane for better chat experience
        JScrollPane scrollPane = new JScrollPane(chatArea);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER); // Disable horizontal scroll
        scrollPane.getVerticalScrollBar().setBackground(new Color(41, 44, 59));
        
        JPanel bottomPanel = new JPanel(new BorderLayout());
        JLabel headPanel = new JLabel("Linsha Chat Bot");
        headPanel.setFont(new Font("Arial", Font.BOLD, 24));
        headPanel.setForeground(Color.WHITE);

        textField = new JTextField();  
        textField.setBackground(new Color(30, 30, 30));
        textField.setForeground(Color.WHITE);
        textField.setFont(new Font("Arial", Font.PLAIN, 14));

        sendButton = createStyledButton("Send");  // Use createStyledButton for consistent styling

        textField.addActionListener(e -> 
        sendMessageToPHP());
        sendButton.addActionListener(e -> sendMessageToPHP());


        bottomPanel.add(textField, BorderLayout.CENTER);
        bottomPanel.add(sendButton, BorderLayout.EAST);
        textPanel.add(headPanel, BorderLayout.NORTH);
        textPanel.add(scrollPane, BorderLayout.CENTER);  // Use scrollPane instead of chatArea
        textPanel.add(bottomPanel, BorderLayout.SOUTH);

        return textPanel;
    }
    private JPanel createButtonPanel() {
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(new Color(41, 44, 59));
        
        JButton menuBtn = createStyledButton("Menu");
        JButton emailBtn = createStyledButton("📩Email");
        JButton apiBtn = createStyledButton("⛓️‍💥API");
        JButton groupBtn = createStyledButton("🗿Group");
        JButton logBtn = createStyledButton("📃Log");
        JButton lightBtn = createStyledButton("💡");
        

        groupBtn.addActionListener(e -> {
            // Java equivalent with faster threading
            startWebBrowserThread("https://t.me/assemly");
        });
        JLabel spacer = new JLabel(""); 
        spacer.setOpaque(false);

        buttonPanel.add(menuBtn);
        buttonPanel.add(spacer);
        buttonPanel.add(emailBtn);
        buttonPanel.add(apiBtn);
        buttonPanel.add(groupBtn);
        buttonPanel.add(logBtn);
        buttonPanel.add(lightBtn);
        
        return buttonPanel;
    }
    private void sendMessageToPHP() {
        String message = textField.getText().trim();
        if (message.isEmpty()) return;
        
        appendToChat("You: " + message);
        textField.setText("");
        sendButton.setEnabled(false);
        sendButton.setText("Sending...");

        executorService.submit(() -> {
            try {
                String response = sendPostRequestToPHP(message);
                SwingUtilities.invokeLater(() -> {
                    appendToChat("Lingsha: " + response);
                    sendButton.setText("Send to Lingsha");
                    sendButton.setEnabled(true);
                });
            } catch (Exception e) {
                SwingUtilities.invokeLater(() -> {
                    appendToChat("Error: " + e.getMessage());
                    sendButton.setText("Send to Lingsha");
                    sendButton.setEnabled(true);
                });
                System.err.println("Error: " + e.getMessage());
            }
        });
    }
    private JPanel createAutoPostPanel() {
        JPanel autoPostPanel = new JPanel(new BorderLayout());
        autoPostPanel.setBackground(new Color(41, 44, 59));

        // Create a panel for multiple buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(new Color(41, 44, 59));

        // Button to open LD Players only
        JButton openLDBtn = createStyledButton("Open LD");
        openLDBtn.addActionListener(e -> {
            // Provide immediate feedback
            openLDBtn.setText("Opening...");
            openLDBtn.setEnabled(false);
            
            startThread(() -> {
                System.out.println("Opening LD Player instances only...");
                runOptionCommand("open_ld", "2"); // Open 2 LD instances
                
                // Re-enable button on UI thread
                SwingUtilities.invokeLater(() -> {
                    openLDBtn.setText("Open LD");
                    openLDBtn.setEnabled(true);
                });
            });
        });


        // Button for full start (LD + Appium)
        JButton fullStartBtn = createStyledButton("Full Start");
        fullStartBtn.addActionListener(e -> {
            fullStartBtn.setText("Starting...");
            fullStartBtn.setEnabled(false);
            
            // Method 1: Direct ExecutorService usage
            executorService.submit(() -> {
                try {
                    System.out.println("Starting full setup: LD Players + Appium servers...");
                    runOptionCommand("full_start", "2");
                    
                    // Update UI on EDT thread
                    SwingUtilities.invokeLater(() -> {
                        fullStartBtn.setText("Full Start");
                        fullStartBtn.setEnabled(true);
                    });
                } catch (Exception ex) {
                    SwingUtilities.invokeLater(() -> {
                        fullStartBtn.setText("Error!");
                        fullStartBtn.setEnabled(true);
                    });
                    ex.printStackTrace();
                }
            });
        });

        // Button to setup LD Players
        JButton setupBtn = createStyledButton("Setup LD");
        setupBtn.addActionListener(e -> {
            startThread(() -> {
                System.out.println("Setting up LD Players...");
                runOptionCommand("setup", "2");
            });
        });

        // Button to test Option class
        JButton testBtn = createStyledButton("Run");
        testBtn.addActionListener(e -> {
            startThread(() -> {
                System.out.println("Remote Option class...");
                runOptionCommand("remote" ,"2");
            });
        });

        buttonPanel.add(openLDBtn);
        buttonPanel.add(setupBtn);
        buttonPanel.add(testBtn);
        buttonPanel.add(fullStartBtn);
        
        autoPostPanel.add(buttonPanel, BorderLayout.CENTER);
        
        return autoPostPanel;
    }
    private String sendPostRequestToPHP(String message) {
        try {
            URL url = URI.create(PHP_API_URL).toURL(); // Modern approach
            HttpURLConnection connection = (HttpURLConnection) url.openConnection(); // Use HttpURLConnection for HTTP
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setDoOutput(true);
            connection.setConnectTimeout(10000); // 10 seconds
            connection.setReadTimeout(30000);    // 30 seconds
            
            String postData = "prompt=" + URLEncoder.encode(message, StandardCharsets.UTF_8.toString());

            try (DataOutputStream writer = new DataOutputStream(connection.getOutputStream())) {
                writer.writeBytes(postData);
                writer.flush();
            }
            
            int responseCode = connection.getResponseCode();
            if (responseCode != 200) {
                throw new Exception("HTTP Error: " + responseCode + " - " + connection.getResponseMessage());
            }

            StringBuilder response = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
            }

            aiResponse = response.toString();
            aiResponseList.add(aiResponse);
            messageList.add(message);

            return aiResponse;

        } catch (ConnectException e) {
            return "Error: Cannot connect to PHP server. Make sure PHP server is running on " + PHP_API_URL;
        } catch (Exception e) {
            e.printStackTrace();
            return "Error: " + e.getMessage();
        }
    }
    private void appendToChat(String message) {
        chatArea.append(message + "\n");
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }

    private JButton createStyledButton(String text) {
        JButton button = new JButton(text);
        button.setBackground(new Color(0x3d11dc)); // Purple color without alpha channel
        button.setForeground(Color.WHITE);
        button.setFocusPainted(false);
        button.setBorderPainted(false);
        button.setMargin(new Insets(5, 5, 5, 5));
        
        // Hover effect using method references (reduces anonymous classes)
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(0x5a1ee6)); // Lighter purple on hover
            }
            @Override
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(0x3d11dc)); // Original purple
            }
        });
        
        return button;
    }

    // OPTIMIZED JAVA WEBBROWSER THREADING
    // This is faster than Python's webbrowser.open with threading
    private void startWebBrowserThread(String url) {
        // Use CompletableFuture for faster execution
        CompletableFuture.runAsync(() -> {
            try {
                // Java's Desktop.browse() is faster than Python's webbrowser.open
                if (Desktop.isDesktopSupported()) {
                    Desktop desktop = Desktop.getDesktop();
                    if (desktop.isSupported(Desktop.Action.BROWSE)) {
                        desktop.browse(new URI(url));
                        System.out.println("Opened URL in browser: " + url);
                    } else {
                        // Fallback for systems without desktop support
                        openURLFallback(url);
                    }
                } else {
                    openURLFallback(url);
                }
            } catch (Exception ex) {
                System.err.println("Error opening browser: " + ex.getMessage());
                // Try fallback method
                openURLFallback(url);
            }
        }, executorService); // Use thread pool for better performance
    }

    // Fallback method using ProcessBuilder (modern approach)
    private void openURLFallback(String url) {
        try {
            String os = System.getProperty("os.name").toLowerCase();
            ProcessBuilder processBuilder;
            
            if (os.contains("win")) {
                // Windows
                processBuilder = new ProcessBuilder("rundll32", "url.dll,FileProtocolHandler", url);
            } else if (os.contains("mac")) {
                // macOS
                processBuilder = new ProcessBuilder("open", url);
            } else {
                // Linux/Unix
                processBuilder = new ProcessBuilder("xdg-open", url);
            }
            
            processBuilder.start();
            System.out.println("Opened URL using fallback method: " + url);
        } catch (Exception e) {
            System.err.println("Fallback browser opening failed: " + e.getMessage());
        }
    }

    private void runPythonScript(String scriptPath) {
        try {
            // Use the correct Python executable path
            ProcessBuilder processBuilder = new ProcessBuilder(
                "python", 
                scriptPath
            );
            processBuilder.redirectErrorStream(true);
            
            Process process = processBuilder.start();
            
            // Read output in real-time
            try (java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream()))) {
                
                String line;
                System.out.println("Python script output:");
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            }
            
            int exitCode = process.waitFor();
            System.out.println("Python script finished with exit code: " + exitCode);
            
        } catch (Exception e) {
            System.err.println("Error running Python script: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // Method to automatically start PHP server when GUI opens
    private void startPHPServer() {
        try {
            // Check if PHP server is already running
            if (isPHPServerRunning()) {
                System.out.println("PHP server is already running on port 8080");
                return;
            }
            
            System.out.println("Starting PHP development server...");
            
            // Get current working directory (where chatBot.php is located)
            String workingDir = System.getProperty("user.dir");
            
            ProcessBuilder processBuilder = new ProcessBuilder(
                "php", "-S", "127.0.0.1:8080"
            );
            processBuilder.directory(new java.io.File(workingDir));
            processBuilder.redirectErrorStream(true);
            
            // Start the PHP server process
            phpServerProcess = processBuilder.start();
            
            // Give it a moment to start
            Thread.sleep(2000);
            
            // Verify it started successfully
            if (isPHPServerRunning()) {
                System.out.println("✅ PHP server started successfully on http://127.0.0.1:8080");
            } else {
                System.err.println("❌ Failed to start PHP server");
            }
            
        } catch (Exception e) {
            System.err.println("Error starting PHP server: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    // Helper method to check if PHP server is running
    private boolean isPHPServerRunning() {
        try {
            URL url = URI.create("http://127.0.0.1:8080").toURL();
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(2000); // 2 seconds timeout
            connection.setReadTimeout(2000);
            
            int responseCode = connection.getResponseCode();
            connection.disconnect();
            
            // Any response (even 404) means server is running
            return responseCode > 0;
        } catch (Exception e) {
            return false;
        }
    }

    // Method to run Option class commands with better performance
    private void runOptionCommand(String command, String... args) {
        try {
            // Build command array
            java.util.List<String> commandList = new java.util.ArrayList<>();
            commandList.add("C:/Users/User/.pyenv/pyenv-win/versions/3.10.11/python.exe");
            commandList.add("-u"); // Unbuffered output for real-time feedback
            commandList.add("run_option.py");
            commandList.add(command);
            
            // Add arguments if provided
            for (String arg : args) {
                commandList.add(arg);
            }
            
            ProcessBuilder processBuilder = new ProcessBuilder(commandList);
            processBuilder.redirectErrorStream(true);
            
            System.out.println("Starting: " + String.join(" ", commandList));
            Process process = processBuilder.start();
            
            // Read output in real-time with immediate flushing
            try (java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream()))) {
                
                String line;
                while ((line = reader.readLine()) != null) {
                    final String output = line; // For lambda
                    SwingUtilities.invokeLater(() -> {
                        System.out.println(output); // Update UI thread safely
                    });
                }
            }
            
            int exitCode = process.waitFor();
            System.out.println("Process finished with exit code: " + exitCode);
            
        } catch (Exception e) {
            System.err.println("Error running Option command: " + e.getMessage());
            e.printStackTrace();
        }
    }
    


    // Method 2: Using ExecutorService with Future for return values
    private void runTaskWithResult() {
        // Submit task that returns a value
        Future<String> future = executorService.submit(() -> {
            // This runs in background thread
            Thread.sleep(2000); // Simulate work
            return "Task completed successfully!";
        });
        
        // Handle the result in another background thread
        executorService.submit(() -> {
            try {
                String result = future.get(); // Wait for result
                SwingUtilities.invokeLater(() -> {
                    System.out.println("Result: " + result);
                });
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    // Method 3: ExecutorService with timeout
    private void runTaskWithTimeout() {
        Future<Void> future = executorService.submit(() -> {
            runOptionCommand("open_ld", "1");
            return null;
        });
        
        executorService.submit(() -> {
            try {
                future.get(30, java.util.concurrent.TimeUnit.SECONDS); // 30 second timeout
                SwingUtilities.invokeLater(() -> {
                    System.out.println("Task completed within timeout");
                });
            } catch (java.util.concurrent.TimeoutException e) {
                future.cancel(true); // Cancel the task
                SwingUtilities.invokeLater(() -> {
                    System.out.println("Task timed out and was cancelled");
                });
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    // Method 4: Schedule delayed tasks
    private void scheduleDelayedTask() {
        // Convert to ScheduledExecutorService for scheduling
        if (executorService instanceof java.util.concurrent.ScheduledExecutorService) {
            java.util.concurrent.ScheduledExecutorService scheduler = 
                (java.util.concurrent.ScheduledExecutorService) executorService;
            
            scheduler.schedule(() -> {
                SwingUtilities.invokeLater(() -> {
                    System.out.println("Delayed task executed!");
                });
            }, 5, java.util.concurrent.TimeUnit.SECONDS); // Run after 5 seconds
        }
    }

    private void startThread(Runnable task) {
        // Show loading indicator or disable button temporarily
        CompletableFuture.runAsync(task, executorService)
            .thenRun(() -> {
                // Re-enable UI components after completion
                SwingUtilities.invokeLater(() -> {
                    System.out.println("Operation completed - UI ready");
                });
            })
            .exceptionally(throwable -> {
                SwingUtilities.invokeLater(() -> {
                    System.err.println("Operation failed: " + throwable.getMessage());
                });
                throwable.printStackTrace();
                return null;
            });
    }

    private void startTimer() {
        startTime = System.currentTimeMillis();
        timer = new Timer(500, e -> updateTime());
        timer.start();
    }

    private void updateTime() {
        long elapsed = (System.currentTimeMillis() - startTime) / 1000;
        long hours = elapsed / 3600;
        long minutes = (elapsed % 3600) / 60;
        long seconds = elapsed % 60;
        
        timeLabel.setText(String.format("%02d:%02d:%02d", hours, minutes, seconds));
    }

    @Override
    public void dispose() {
        // Stop PHP server when application closes
        if (phpServerProcess != null && phpServerProcess.isAlive()) {
            System.out.println("Stopping PHP server...");
            phpServerProcess.destroy();
            try {
                // Wait up to 5 seconds for graceful shutdown
                if (!phpServerProcess.waitFor(5, java.util.concurrent.TimeUnit.SECONDS)) {
                    System.out.println("Force killing PHP server...");
                    phpServerProcess.destroyForcibly();
                }
                System.out.println("PHP server stopped");
            } catch (InterruptedException e) {
                phpServerProcess.destroyForcibly();
            }
        }
        
        if (timer != null) {
            timer.stop();
        }
        if (executorService != null) {
            executorService.shutdown();
        }
        super.dispose();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new LDPlayerGUI().setVisible(true);
        });
    }
}
