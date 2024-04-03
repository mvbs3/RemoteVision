import "./App.css";
import VideoCapture from "./Components/VideoCapture";
import Header from "./Components/Header";
import Box from "@mui/material/Box";
function App() {
  return (
    <div className="App">
      <Box sx={{ bgcolor: "#cfe8fc", height: "100vh" }}>
        <Header></Header>
        <VideoCapture></VideoCapture>
      </Box>
    </div>
  );
}

export default App;
