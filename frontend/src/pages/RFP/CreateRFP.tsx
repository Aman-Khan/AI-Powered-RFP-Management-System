import { useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  TextField,
  Typography,
  Paper,
  Stack,
} from "@mui/material";
import toast from "react-hot-toast";
import { api } from "../../lib/axios";

export default function CreateRFP() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [structured, setStructured] = useState<any>(null);

  const userId = localStorage.getItem("userId");

  const generateRFP = async () => {
    if (!input.trim()) {
      toast.error("Please enter RFP details");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/rfp/create", {
        text: input,
        userId,
      });

      setStructured(res.data.structuredRequirements);
      toast.success("RFP generated successfully!");

    } catch (err) {
      toast.error("Failed to generate RFP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} mb={1}>
        Create RFP
      </Typography>

      <Typography variant="body1" color="text.secondary" mb={2}>
        Describe your procurement needs and let AI convert them into a structured RFP.
      </Typography>

      <TextField
        multiline
        minRows={6}
        fullWidth
        placeholder="Example: We need 20 laptops (16GB RAM), 15 monitors (27-inch), delivery in 30 days..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}               // 🔒 Disable during loading
        sx={{ mb: 3 }}
      />

      <Stack direction="row" justifyContent="flex-end">
        <Button
          variant="contained"
          size="large"
          onClick={generateRFP}
          disabled={loading}             // 🔒 Disable button while generating
          startIcon={
            loading ? <CircularProgress size={20} color="inherit" /> : undefined
          }
          sx={{
            textTransform: "none",
            fontWeight: 600,
            px: 4,
          }}
        >
          {loading ? "Processing..." : "Generate RFP"}
        </Button>
      </Stack>

      {structured && (
        <>
          <Typography variant="h6" fontWeight={700} mt={4} mb={2}>
            AI-Generated Structured RFP
          </Typography>

          <Paper
            elevation={2}
            sx={{
              p: 3,
              background: "#f8f9fa",
              borderRadius: 2,
              whiteSpace: "pre-wrap",
              fontFamily: "monospace",
              fontSize: 14,
            }}
          >
            {JSON.stringify(structured, null, 2)}
          </Paper>
        </>
      )}
    </Box>
  );
}
