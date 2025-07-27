import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.UIManager;

public class LDPlayerGUIWithPHP extends JFrame {
    private JLabel timeLabel;
    private Timer timer;
    private ExecutorService executorService;
    private JTextArea chatArea;
    private JTextField inputField;
    private JButton sendButton;
    
    // PHP API URL - Force IPv4
    private static final String PHP_API_URL = "http://127.0.0.1:8080/chatBot.php";
    
    public LDPlayerGUIWithPHP() {
        setTitle("LDPlayer GUI with PHP Communication");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        
        // Initialize ExecutorService
        executorService = Executors.newCachedThreadPool();
        
        initComponents();
        startTimer();
        setVisible(true);
    }
    
    private void initComponents() {
        // Top panel with time
        JPanel topPanel = new JPanel(new FlowLayout());
        topPanel.setBackground(new Color(45, 45, 45));
        timeLabel = new JLabel();
        timeLabel.setForeground(Color.WHITE);
        timeLabel.setFont(new Font("Arial", Font.BOLD, 16));
        topPanel.add(timeLabel);
        add(topPanel, BorderLayout.NORTH);
        
        // Center panel - Chat area
        chatArea = new JTextArea(20, 50);
        chatArea.setEditable(false);
        chatArea.setBackground(new Color(30, 30, 30));
        chatArea.setForeground(Color.WHITE);
        chatArea.setFont(new Font("Arial", Font.PLAIN, 14));
        JScrollPane scrollPane = new JScrollPane(chatArea);
        add(scrollPane, BorderLayout.CENTER);
        
        // Bottom panel - Input
        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.setBackground(new Color(45, 45, 45));
        
        inputField = new JTextField();
        inputField.setBackground(new Color(60, 60, 60));
        inputField.setForeground(Color.WHITE);
        inputField.setFont(new Font("Arial", Font.PLAIN, 14));
        
        sendButton = new JButton("Send to Lingsha");
        sendButton.setBackground(new Color(0, 120, 215));
        sendButton.setForeground(Color.WHITE);
        sendButton.setFocusPainted(false);
        
        // Add action listeners
        sendButton.addActionListener(e -> sendMessageToPHP());
        inputField.addActionListener(e -> sendMessageToPHP());
        
        bottomPanel.add(inputField, BorderLayout.CENTER);
        bottomPanel.add(sendButton, BorderLayout.EAST);
        add(bottomPanel, BorderLayout.SOUTH);
        
        pack();
        setLocationRelativeTo(null);
    }
    
    private void sendMessageToPHP() {
        String message = inputField.getText().trim();
        if (message.isEmpty()) return;
        
        // Add user message to chat
        appendToChat("You: " + message);
        inputField.setText("");
        sendButton.setEnabled(false);
        sendButton.setText("Sending...");
        
        // Send message in background thread
        executorService.submit(() -> {
            try {
                String response = sendPostRequestToPHP(message);
                
                // Update UI on EDT
                SwingUtilities.invokeLater(() -> {
                    appendToChat("Lingsha: " + response);
                    sendButton.setEnabled(true);
                    sendButton.setText("Send to Lingsha");
                });
                
            } catch (Exception e) {
                SwingUtilities.invokeLater(() -> {
                    appendToChat("Error: " + e.getMessage());
                    sendButton.setEnabled(true);
                    sendButton.setText("Send to Lingsha");
                });
            }
        });
    }
    
    private String sendPostRequestToPHP(String prompt) throws Exception {
        try {
            URL url = new URL(PHP_API_URL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setDoOutput(true);
            connection.setConnectTimeout(10000); // 10 seconds
            connection.setReadTimeout(30000);    // 30 seconds
            
            // Send data
            String postData = "prompt=" + URLEncoder.encode(prompt, StandardCharsets.UTF_8.toString());
            try (DataOutputStream writer = new DataOutputStream(connection.getOutputStream())) {
                writer.writeBytes(postData);
                writer.flush();
            }
            
            // Check response code
            int responseCode = connection.getResponseCode();
            if (responseCode != 200) {
                throw new Exception("HTTP Error: " + responseCode + " - " + connection.getResponseMessage());
            }
            
            // Read response
            StringBuilder response = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
            }
            
            return response.toString();
            
        } catch (ConnectException e) {
            throw new Exception("Cannot connect to PHP server. Make sure PHP server is running on " + PHP_API_URL);
        } catch (Exception e) {
            throw new Exception("Network error: " + e.getMessage());
        }
    }
    
    private void appendToChat(String message) {
        chatArea.append(message + "\n");
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }
    
    private void startTimer() {
        timer = new Timer(1000, e -> {
            java.util.Date now = new java.util.Date();
            timeLabel.setText(String.format("%tT", now));
        });
        timer.start();
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
            new LDPlayerGUIWithPHP();
        });
    }
}
