import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
import { CookiesProvider } from 'react-cookie';
import { PaySeller } from "./PaySeller/PaySeller";
import { SellerPage } from "./Seller/Seller";

function App() {
  return (
    <CookiesProvider>
      <Router>
        <Switch>
          <Route
            path="/pay/:sellerHandle"
            render={({ match }) => (
              <PaySeller sellerHandle={match.params.sellerHandle} />
            )}
          />
          <Route
            path="/seller/:sellerId"
            render={({ match }) => <SellerPage sellerId={match.params.sellerId} />}
          />
        </Switch>
      </Router>
    </CookiesProvider>
  );
}

export default App;
