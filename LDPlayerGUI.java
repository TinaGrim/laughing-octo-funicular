import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CompletableFuture;
import java.net.URI;

public class LDPlayerGUI extends JFrame {
    private JLabel timeLabel;
    private Timer timer;
    private long startTime;
    private ExecutorService executorService;

    public LDPlayerGUI() {
        // Initialize executor service for faster threading
        executorService = Executors.newCachedThreadPool();
        
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
        
        tabbedPane.addTab("Devices", new JLabel("Hello"));
        tabbedPane.addTab("Auto Post", createAutoPostPanel());
        
        mainPanel.add(leftPanel, BorderLayout.WEST);
        mainPanel.add(tabbedPane, BorderLayout.CENTER);
        
        add(mainPanel);
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
        
        leftPanel.add(headerPanel, BorderLayout.NORTH);
        leftPanel.add(buttonPanel, BorderLayout.SOUTH);
        
        return leftPanel;
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
        
        // THIS IS THE MAIN CONVERSION: Python webbrowser threading to Java
        // Python: Group.clicked.connect(lambda: self.start_thread(webbrowser.open, "https://t.me/assemly"))
        groupBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Java equivalent with faster threading
                startWebBrowserThread("https://t.me/assemly");
            }
        });
        
        buttonPanel.add(menuBtn);
        buttonPanel.add(emailBtn);
        buttonPanel.add(apiBtn);
        buttonPanel.add(groupBtn);
        buttonPanel.add(logBtn);
        buttonPanel.add(lightBtn);
        
        return buttonPanel;
    }

    private JPanel createAutoPostPanel() {
        JPanel autoPostPanel = new JPanel(new BorderLayout());
        autoPostPanel.setBackground(new Color(41, 44, 59));
        
        JLabel label = new JLabel("Auto Post Panel");
        label.setForeground(Color.WHITE);
        label.setHorizontalAlignment(SwingConstants.CENTER);
        
        autoPostPanel.add(label, BorderLayout.CENTER);
        
        return autoPostPanel;
    }

    private JButton createStyledButton(String text) {
        JButton button = new JButton(text);
        button.setBackground(new Color(19, 89, 157)); // #13599d
        button.setForeground(Color.WHITE);
        button.setFocusPainted(false);
        button.setBorderPainted(false);
        button.setMargin(new Insets(5, 5, 5, 5));
        
        // Hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(23, 110, 195)); // #176ec3
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(19, 89, 157));
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

    // Fallback method using Runtime.exec (similar to Python's webbrowser)
    private void openURLFallback(String url) {
        try {
            String os = System.getProperty("os.name").toLowerCase();
            Runtime runtime = Runtime.getRuntime();
            
            if (os.contains("win")) {
                // Windows
                runtime.exec("rundll32 url.dll,FileProtocolHandler " + url);
            } else if (os.contains("mac")) {
                // macOS
                runtime.exec("open " + url);
            } else {
                // Linux/Unix
                runtime.exec("xdg-open " + url);
            }
            System.out.println("Opened URL using fallback method: " + url);
        } catch (Exception e) {
            System.err.println("Fallback browser opening failed: " + e.getMessage());
        }
    }

    // Generic method to start any thread (equivalent to Python's start_thread)
    private void startThread(Runnable task) {
        CompletableFuture.runAsync(task, executorService)
            .exceptionally(throwable -> {
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
