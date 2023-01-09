import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Posts from "./Posts"




export default function App() {
    return (
        <Router>

            <Routes>
                <Route path="/" element={<Posts />}/>
            </Routes>

        </Router>
    )
}