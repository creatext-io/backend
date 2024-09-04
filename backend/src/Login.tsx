import React, { useState } from "react";
import { Formik, Field } from "formik";
import axios from "axios";
import { blackA, whiteA } from "@radix-ui/colors";
import { styled } from "@stitches/react";
import * as Label from "@radix-ui/react-label";
import { useNavigate } from "react-router-dom";
import SvgIcon from "./assets/scrible-logo.svg";
function Login() {
  const navigate = useNavigate();

  const [errorMsg, setErrorMsg] = useState("");

  const onSubmit = (data) => {
    const fd = new FormData();
    fd.append("username", data.email);
    fd.append("password", data.accessKey);
    axios
      .post(`${import.meta.env.VITE_BASE_API}/login`, fd)
      .then((res) => {
        window.localStorage.setItem("userId", res.data.data);
        navigate("/dashboard");
      })
      .catch((err) => {
        setErrorMsg(err?.response?.data?.detail);
        setTimeout(() => {
          setErrorMsg("");
        }, 5000);
      });
  };
  return (
    <div className="login-container relative bg-gray-100 ">
      <header className="flex items-center justify-between py-4 min-h-[72px] px-4">
        <div className="flex items-center"></div>
        <div className="flex items-center">
          <p className="text-sm text-slate-500 cursor-pointer">
            New to Scrible?
          </p>
          <button
            onClick={() => navigate("/signup")}
            className="text-sm border-solid border text-sm border-slate-300 ml-4 py-1.5 px-2 text-slate-600 shadow-sm rounded"
          >
            Create an account
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
              accessKey: "",
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
                  <LabelRoot htmlFor="accessKey">Password</LabelRoot>
                  <Input
                    type="password"
                    id="accessKey"
                    name="accessKey"
                    placeholder="enter password"
                    onChange={handleChange}
                    value={values.accessKey}
                  />
                </div>

                <button
                  type="submit"
                  className={`mt-8  text-sm border-solid border ${
                    errorMsg ? "bg-red-400" : "bg-[#12c55f]"
                  }  text-sm font-light p-2 text-slate-100 rounded w-full`}
                >
                  <span className="font-bold">{errorMsg || "Login"}</span>
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

export default Login;
