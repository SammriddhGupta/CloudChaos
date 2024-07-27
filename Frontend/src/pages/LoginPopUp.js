import React from "react";
import { Modal, Box, Typography, Button } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

function LoginPopup({ open }) {

    const navigate = useNavigate();

    const handleClose = () => {
        navigate('/landing');
    };

  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Typography id="modal-modal-title" variant="h6" component="h2">
          Login Required
        </Typography>
        <Typography id="modal-modal-description" sx={{ mt: 2 }}>
          You need to be logged in to access this feature.
        </Typography>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Link to="https://cloudchaos.auth.ap-southeast-2.amazoncognito.com/login?client_id=1gqsqb0d5vh6osuuc2950ub8v9&response_type=token&scope=email+openid+phone&redirect_uri=https://main.d332b7vcir4cg5.amplifyapp.com/redirect" className="signup-button">
            <Button variant="contained" sx={{ mt: 2, bgcolor: '#53287a' }}>
              Login
            </Button>
          </Link>

          <Button variant="contained" color="grey" onClick={handleClose} sx={{ mt: 2 }}>
            Cancel
          </Button>
        </div>
      </Box>
    </Modal>
  );
}

export default LoginPopup;