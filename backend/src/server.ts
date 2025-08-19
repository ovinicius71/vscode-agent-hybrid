import express from "express";
import bodyParser from "body-parser";

const app = express();
app.use(bodyParser.json());

app.post("/complete", (req, res) => {
    const { file_text, cursor_pos, top_k } = req.body;
    // Retorna um completion com base nos ultimos 50 chars
    const context = (file_text || "").slice(Math.max(0, cursor_pos - 50), cursor_pos);
    const completion = `/* suggestion based on: "${context.replace(/\n/g, ' ')}" */\nconsole.log('hello from mock');`;
    res.json({ completion });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Backend is running on port ${PORT}`);
});