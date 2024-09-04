import { styled } from "@stitches/react";
import { Navigate, useOutlet, useNavigate } from "react-router-dom";
import Logo from "../assets/scrible-editor-logo.svg";
import { HomeIcon, ExitIcon, SymbolIcon } from "@radix-ui/react-icons";

const Navbar = styled("nav", {
  position: "fixed",
  width: "100%",
  display: "flex",
  justifyContent: "space-between",
  background: "#7A7FD3",
  borderBottom: "1px solid rgb(239, 241, 244)",
  padding: "1rem 1rem",
  alignItems: "center",
  zIndex: "999",
});

const MainContainer = styled("main", {
  paddingTop: "100px",
});

const IconWrapper = styled("div", {
  width: "90px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "0.5rem 1rem",
});

const HeaderIconWrapper = styled("div", {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
});
const SavingLoader = styled("div", {
  width: "50px",
  height: "50px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  color: "#ffffff",
  scale: "2",
});

export const ProtectedLayout = () => {
  //   const { user } = useAuth();
  const outlet = useOutlet();

  const navigate = useNavigate();

  if (!window.localStorage.getItem("userId")) {
    return <Navigate to="/" />;
  }

  return (
    <div>
      <Navbar>
        <HeaderIconWrapper>
          <img src={Logo} />
        </HeaderIconWrapper>
        <IconWrapper>
          <button className="text-white">
            <HomeIcon
              className="scale-100"
              onClick={() => {
                navigate("/dashboard");
              }}
            />
          </button>
          <button
            onClick={() => {
              window.localStorage.removeItem("userId");
              navigate("/login");
            }}
            className="text-white"
          >
            <ExitIcon className="scale-100" />
          </button>
        </IconWrapper>
      </Navbar>
      <MainContainer>{outlet}</MainContainer>
    </div>
  );
};
