import { FC } from "react";
import {BrowserRouter, Route} from "react-router-dom";
import NewVinyl from "./components/NewVinyl";
import SearchVinyl from "./components/SearchVinyl";
import Header from "./components/Header";

const App: FC = () => {
    return (
        <BrowserRouter>
            <Header/>
            <Route path="/" exact component={NewVinyl}/>
            <Route path="/search" component={SearchVinyl}/>
        </BrowserRouter>
    )
}
export default App;