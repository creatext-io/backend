import React from "react";
import { Formik, Field } from "formik";
import axios from "axios";
import { blackA, whiteA } from "@radix-ui/colors";
import { styled } from "@stitches/react";
import * as Label from "@radix-ui/react-label";
import { useNavigate } from "react-router-dom";
import SvgIcon from "./assets/scrible-logo.svg";
function Signup() {
  const navigate = useNavigate();

  const onSubmit = (data) => {
    const fd = new FormData();
    fd.append("username", data.email);
    fd.append("password", data.password);
    axios
      .post(`${import.meta.env.VITE_BASE_API}/signup`, fd)
      .then((res) => {
        window.localStorage.setItem("userId", res.data.data);
        navigate("/login");
      })
      .catch(console.log);
  };
  return (
    <div className="login-container relative bg-gray-100 ">
      <header className="flex items-center justify-between py-4 min-h-[72px] px-4">
        <div className="flex items-center"></div>
        <div className="flex items-center">
          <p className="text-sm text-slate-500 cursor-pointer">
            Already have an account?
          </p>
          <button
            onClick={() => navigate("/login")}
            className="text-sm border-solid border text-sm border-slate-300 ml-4 py-1.5 px-2 text-slate-600 shadow-sm rounded"
          >
            Login
          </button>
        </div>
      </header>
      <div className="h-[calc(100vh_-_144px)] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center w-72 border-1 p-8 rounded-lg bg-white shadow-sm shadow-gray-400 ">
          <img src={SvgIcon} className="w-24 mb-10" />
          <Formik
            onSubmit={onSubmit}
            initialValues={{
              email: "",
              password: "",
            }}
          >
            {({
              values,
              errors,
              touched,
              handleSubmit,
              isSubmitting,
              handleChange,
            }) => (
              <form onSubmit={handleSubmit} className="w-full">
                <div className="flex flex-col">
                  <LabelRoot htmlFor="email">Email</LabelRoot>
                  <Input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="enter email"
                    onChange={handleChange}
                    value={values.email}
                  />
                </div>
                <div className="flex flex-col mt-5">
                  <LabelRoot htmlFor="password">Password</LabelRoot>
                  <Input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="create password"
                    onChange={handleChange}
                    value={values.password}
                  />
                </div>

                <button
                  type="submit"
                  className="mt-8  text-sm border-solid border bg-[#12c55f] text-sm font-light p-2 text-slate-100 rounded w-full"
                >
                  <span className="font-bold">Signup</span>
                </button>
              </form>
            )}
          </Formik>
        </div>
      </div>

      <hr className="w-full h-px border-0 dark:bg-gray-300 absolute" />
      <footer className="flex items-center justify-center py-4 min-h-[72px] px-2">
        <p className="text-xs text-neutral-600 mr-2">© 2023 Scrible</p>
        <div className="flex items-center">
          <p className="text-sm text-[#4e89c0] cursor-pointer mr-2">Terms</p>
          <p className="text-sm text-[#4e89c0] cursor-pointer">Privacy</p>
        </div>
      </footer>
    </div>
  );
}

const LabelRoot = styled(Label.Root, {
  fontSize: 12,
  fontWeight: 500,
  marginBottom: 4,
  color: "rgba(55, 53, 47, 0.65)",
});

const Input = styled("input", {
  all: "unset",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: 6,
  padding: "3px 10px",
  height: 30,
  fontSize: 15,
  lineHeight: 1,
  backgroundColor: "rgba(242, 241, 238, 0.6)",
  boxShadow: `rgb(15 15 15 / 10%) 0px 0px 0px 1px inset`,
  "&:focus": {
    boxShadow: `rgb(35 131 226 / 57%) 0px 0px 0px 1px inset, rgb(35 131 226 / 35%) 0px 0px 0px 2px !important`,
  },
  "&::placeholder": {
    color: "#ababa8",
  },
});

export default Signup;
