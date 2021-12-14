import {
  Button,
  Card,
  CardContent,
  CardHeader,
  TextField,
} from "@material-ui/core";
import { useEffect, useState } from "react";
import { useCookies } from 'react-cookie';

type Seller = {
  id: number;
  name: string;
  handle: string;
}

export const SellerPage = ({ sellerId }: { sellerId: string }) => {
  const [cookies, setCookie] = useCookies(['csrftoken']);
  const [seller, setSeller] = useState<Seller | null>(null);
  const [fetchSellerError, setFetchSellerError] = useState<string | null>(null);
  const [sellerHandleInput, setSellerHandleInput] = useState<string>('');

  useEffect(() => {
    fetch(`/api/sellers/${sellerId}/`)
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to fetch seller");

        const data = await res.json();
        setSeller(data);
        setSellerHandleInput(data.handle);
      })
      .catch((err) => {
        setFetchSellerError(err.message);
      });
  }, [sellerId]);

  if (fetchSellerError) {
    return <div>{fetchSellerError}</div>;
  }

  if (!seller) {
    return <div>pending</div>;
  }

  const onSubmit = () => {
    console.log(seller, sellerHandleInput);
    fetch(`/api/sellers/${sellerId}/`, {
      method: 'PUT',
      body: JSON.stringify({
        ...seller,
        handle: sellerHandleInput,
      }),
      headers: {
             'X-CSRFTOKEN': cookies['csrftoken'],
             'Content-Type': 'application/json',
         },
      })
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to update seller");

        const data = await res.json();
        setSeller(data);
        setSellerHandleInput(data.handle);
      })
      .catch((err) => {
        setFetchSellerError(err.message);
      });
  };

  return (
    <Card>
      <CardHeader title="Edit seller" subheader="Make changes to a seller" />
      <CardContent>
        <form noValidate autoComplete="off">
          <TextField
            id="sellerId"
            label="Seller ID"
            fullWidth={true}
            style={{ margin: 8 }}
            value={seller.id}
            disabled={true}
          />
          <TextField
            id="sellerName"
            label="Seller Name"
            fullWidth={true}
            style={{ margin: 8 }}
            value={seller.name}
            disabled={true}
          />
          <TextField
            id="sellerHandle"
            label="Seller Handle"
            fullWidth={true}
            style={{ margin: 8 }}
            value={sellerHandleInput}
            onChange={(e) => setSellerHandleInput(e.target.value)}
          />
          <Button variant="contained" color="primary" onClick={onSubmit}>
            Update
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};
