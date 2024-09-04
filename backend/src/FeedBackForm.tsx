import React, { useRef, useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { Cross2Icon } from "@radix-ui/react-icons";
import axios from "axios";

export const FeebBackForm = () => {
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const ref = useRef<HTMLButtonElement>(null);

  const onSubmit = () => {
    if (text.length === 0) return setError("Feeback is required !");
    setIsSubmitting(true);
    const userId = localStorage.getItem("userId");
    const fd = new FormData();
    fd.append("text", text);
    fd.append("user_id", "1234");
    axios
      .post(`${import.meta.env.VITE_BASE_API}/feedback`, fd, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userId}`,
        },
      })
      .then((res) => {
        setIsSubmitting(false);
        // eslint-disable-next-line no-unused-expressions
        ref?.current?.click();
      })
      .catch((err) => {
        setIsSubmitting(false);
        setError(err?.response?.data?.detail);
      });
  };

  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <p className=" text-xs text-blue-500 hover:underline cursor-pointer ">
          Give feedback or bug?
        </p>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="bg-blackA9 data-[state=open]:animate-overlayShow fixed inset-0" />
        <Dialog.Content className="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white p-[25px] shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] focus:outline-none">
          <Dialog.Title className="text-mauve12 m-0 text-[17px] font-medium">
            Give feedback or bug?
          </Dialog.Title>
          <Dialog.Description className="text-mauve11 mt-[10px] mb-5 text-[15px] leading-normal">
            Found something that is not working. let us know.
          </Dialog.Description>

          <div className="flex justify-between">
            <label className="text-[15px] font-medium leading-[35px] text-black">
              Question
            </label>
            <label className="text-[15px] font-medium leading-[35px] text-red-500">
              {error}
            </label>
          </div>

          <textarea
            className={`box-border w-full bg-blackA5  inline-flex appearance-none items-center justify-center rounded-[4px] p-[10px] text-[15px] leading-none text-black 
            outline-none 
            selection:color-white selection:bg-blackA9 resize-none 
            shadow-[0_0_0_1px_${error ? "red" : ""}]
        
            hover:shadow-[0_0_0_1px_${error ? "red" : "black"}] 
            focus:shadow-[0_0_0_2px_${error ? "red" : "black"}] 
            `}
            required
            onChange={(e) => {
              setError("");
              setText(e.target.value);
            }}
          />

          <div className="mt-[25px] flex justify-end">
            <button
              disabled={isSubmitting}
              onClick={onSubmit}
              className="bg-green4 text-green11 hover:bg-green5 focus:shadow-green7 inline-flex h-[35px] items-center justify-center rounded-[4px] px-[15px] font-medium leading-none focus:shadow-[0_0_0_2px] focus:outline-none"
            >
              {isSubmitting ? "Submitting..." : "Send"}
            </button>
          </div>
          <Dialog.Close asChild>
            <button
              className="text-violet11 hover:bg-violet4 focus:shadow-violet7 absolute top-[10px] right-[10px] inline-flex h-[25px] w-[25px] appearance-none items-center justify-center rounded-full focus:shadow-[0_0_0_2px] focus:outline-none"
              aria-label="Close"
              ref={ref}
            >
              <Cross2Icon />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
