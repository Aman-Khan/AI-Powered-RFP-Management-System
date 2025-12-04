import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../lib/axios";
import PersonIcon from "@mui/icons-material/Person";
import { useToast } from "../../components/Toast/MuiToastProvider";

import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Avatar,
} from "@mui/material";


export default function Login() {
  const [userId, setUserId] = useState("");
  const navigate = useNavigate();
  const { showToast } = useToast();

  const handleLogin = async () => {
    if (!userId.trim()) {
      showToast("User ID is required", "error");
      return;
    }

    try {
      await api.get(`/user/${userId}`);

      localStorage.setItem("userId", userId);
      showToast("Login successful!", "success");

      setTimeout(() => navigate("/"), 600);
    } catch {
      showToast("Invalid User ID. Please try again.", "error");
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "linear-gradient(135deg, #bbdefb 0%, #ffffff 50%, #eeeeee 100%)",
        background: "linear-gradient(135deg, #bbdefb 0%, #ffffff 50%, #eeeeee 100%)",
      }}
    >
      <Card
        elevation={10}
        sx={{
          width: 380,
          p: 4,
          borderRadius: 4,
          backdropFilter: "blur(10px)",
          backgroundColor: "rgba(255,255,255,0.85)",
          animation: "fadeIn 0.6s ease",
        }}
      >
        <CardContent>
          {/* Avatar Icon */}
          <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
            <Avatar sx={{ bgcolor: "#1976d2", width: 64, height: 64 }}>
              <PersonIcon fontSize="large" />
            </Avatar>
          </Box>

          <Typography
            variant="h4"
            align="center"
            fontWeight="bold"
            sx={{ mb: 1 }}
          >
            Welcome Back
          </Typography>

          <Typography
            variant="body2"
            align="center"
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            Please enter your User ID to continue
          </Typography>

          {/* Input */}
          <TextField
            fullWidth
            label="User ID"
            variant="outlined"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            sx={{ mb: 3 }}
          />

          {/* Button */}
          <Button
            fullWidth
            size="large"
            variant="contained"
            onClick={handleLogin}
            sx={{
              py: 1.5,
              fontSize: "1rem",
              fontWeight: "600",
              background: "linear-gradient(to right, #1976d2, #1565c0)",
              "&:hover": {
                background: "linear-gradient(to right, #1565c0, #0d47a1)",
              },
              boxShadow: "0 6px 20px rgba(25,118,210,0.25)",
            }}
          >
            Continue
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}
