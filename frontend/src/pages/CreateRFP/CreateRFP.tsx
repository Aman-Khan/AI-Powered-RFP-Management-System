import { useState } from "react";
import { api } from "../../lib/axios";
import { Button, TextField, Box, Typography, Paper } from "@mui/material";

export default function CreateRFP() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    const res = await api.post("/rfp/generate", { prompt: input });
    setResult(res.data);
    setLoading(false);
  };

  return (
    <Box p={4}>
      <Typography variant="h5" mb={2}>
        Create RFP
      </Typography>

      <TextField
        multiline
        fullWidth
        minRows={4}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your procurement needs..."
      />

      <Button
        variant="contained"
        sx={{ mt: 2 }}
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate RFP"}
      </Button>

      {result && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6">Structured RFP</Typography>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </Paper>
      )}
    </Box>
  );
}
