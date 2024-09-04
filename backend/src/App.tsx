import { useEffect, useState, useRef } from "react";
import ReactQuill from "react-quill";
import _ from "lodash";
import "./App.css";
import "quill/dist/quill.snow.css";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { styled } from "@stitches/react";
import * as Label from "@radix-ui/react-label";
import { v4 as uuidv4 } from "uuid";
import { SymbolIcon } from "@radix-ui/react-icons";
import { FeebBackForm } from "./FeedBackForm";

const tools = [["bold", "italic", "underline"]];

const apiKey = import.meta.env.VITE_APP_API;

const API = apiKey;

const getDocumentById = (docId: string) => {
  return axios.get(`${import.meta.env.VITE_BASE_API}/document/${docId}`, {
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem("userId")}`,
    },
  });
};

const removeAutoCompleteElement = () => {
  const autoCompleteElement = document.querySelectorAll(".ql-editor p span");
  (autoCompleteElement as NodeListOf<HTMLElement>).forEach((el) => {
    if (el.style.color === "rgba(117, 117, 117, 0.3)") {
      el.remove();
    }
  });
};

const TitleInput = styled("input", {
  display: "block",
  width: "100%",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: 6,
  padding: "3px 10px",
  height: 45,
  fontSize: 18,
  lineHeight: 1,
  // backgroundColor: "rgba(242, 241, 238, 0.6)",
  backgroundColor: "white",
  boxShadow: `rgb(15 15 15 / 10%) 0px 0px 0px 1px inset`,
  "&:focus": {
    boxShadow: `rgb(35 131 226 / 57%) 0px 0px 0px 1px inset, rgb(35 131 226 / 35%) 0px 0px 0px 2px !important`,
  },
  "&::placeholder": {
    color: "#ababa8",
  },
});

const LabelRoot = styled(Label.Root, {
  fontSize: 12,
  fontWeight: 500,
  marginBottom: 4,
  color: "rgba(55, 53, 47, 0.65)",
});

const SavingLoader = styled("div", {
  width: "15px",
  height: "15px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
});

function App() {
  const { docId } = useParams();
  const editorText = useRef("");
  const autoComplete = useRef("");
  const keyStroke = useRef(true);
  const quillRef: any = useRef(null);
  const signalRef: any = useRef(null);
  const originalValueRef = useRef("");
  const prevValues = useRef({
    title: "",
    content: "",
  });
  const navigate = useNavigate();
  const [multiLine, setMultiLine] = useState(false);
  const [title, setTitle] = useState<string>("");
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isFetching, setIsFetching] = useState<boolean>(false);

  const cleanText = (str: any) => {
    return str.replace(/(<([^>]+)>)/gi, "");
  };

  const replaceNbsps = (str: any) => {
    return str.replace(/&(nbsp|amp|quot|lt|gt);/g, " ");
  };

  const createEventListeners = () => {
    const quill = quillRef.current.editingArea;
    quill.addEventListener("keydown", (e: any) => {
      if (autoComplete.current) {
        if (e.keyCode == "9") {
          e.preventDefault();

          const autoCompleted = autoComplete.current;
          removeAutoCompleteElement();

          var n = document
            .querySelector(".ql-editor")
            ?.innerHTML.lastIndexOf("</p>");
          var str2 =
            document.querySelector(".ql-editor")?.innerHTML.substring(0, n) +
            autoCompleted.trim() +
            document.querySelector(".ql-editor")?.innerHTML.substring(n || 0);

          quillRef.current.editor.clipboard.dangerouslyPasteHTML(str2, "api");
          autoComplete.current = "";
          quillRef.current.editor.setSelection(
            editorText.current.length + autoCompleted.length
          );
        } else {
          console.log("NOT TAB KEYYYY");
          removeAutoCompleteElement();
          const space = "&nbsp;";

          var n = document
            .querySelector(".ql-editor")
            ?.innerHTML.lastIndexOf("</p>");
          var str2 =
            document.querySelector(".ql-editor")?.innerHTML.substring(0, n) +
            space +
            document.querySelector(".ql-editor")?.innerHTML.substring(n || 0);

          quillRef.current.editor.clipboard.dangerouslyPasteHTML(str2, "api");

          autoComplete.current = "";
          quillRef.current.editor.setSelection(editorText.current.length + 1);
        }
      } else {
        keyStroke.current = true;
      }
    });

    window.addEventListener("click", (e: any) => {
      if (autoComplete.current) {
        const selection = quillRef.current.unprivilegedEditor.getSelection();
        console.log(selection, "SELELTION FROM CLICK");
        removeAutoCompleteElement();
        // quillRef.current.editor.clipboard.dangerouslyPasteHTML(
        //   document.querySelector(".ql-editor")?.innerHTML
        // );
        autoComplete.current = "";
        // quillRef.current.editor.setSelection(selection.index);
      }
    });
  };

  useEffect(() => {
    createEventListeners();

    if (docId) {
      getDocumentById(docId).then((res) => {
        console.log(res, "GET DOC BY ID");
        originalValueRef.current = res.data.data[0].body;
        editorText.current = res.data.data[0].body;
        setTitle(res.data.data[0].title);
        prevValues.current.content = res.data.data[0].body;
        prevValues.current.title = res.data.data[0].title;

        quillRef.current.editor.clipboard.dangerouslyPasteHTML(
          0,
          res.data.data[0].body
        );
      });
    } else {
      const newUUID = uuidv4();
      navigate(`/editor/${newUUID}`);
    }
  }, []);

  const handleFetch = async (val: any) => {
    // Get the current selection from the editor
    const selection = quillRef.current.unprivilegedEditor.getSelection();
    console.log(val, "VALUUEUEUE");
    // If we haven't pressed a key yet or there is no value, then exit the function
    if (!keyStroke.current || !val) {
      return;
    }
    // Store the text from the editor and remove any non-breaking spaces
    const text = replaceNbsps(cleanText(val));
    // Create the payload to send to the API
    const payload = {
      text: text.trim(),
      doc_id: docId,
      cursor_position: selection.index,
    };

    /*
      Abort if the cursor is not at the end of the current text.
    */
    if (selection.index !== text.length) {
      return;
    }
    if (
      // If the text is not the same as the original value
      text.trim() !== replaceNbsps(cleanText(originalValueRef.current)).trim()
    ) {
      // Create a new AbortController signal
      signalRef.current = new AbortController();
      // Fetch the data from the API
      setIsFetching(true);
      const data = await fetch(API, {
        signal: signalRef.current.signal,
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${window.localStorage.getItem("userId")}`,
        },
      });
      // Wait for the response and parse the JSON
      const value = await data.json();
      setIsFetching(false);
      /*
      Checking if there is even a completion at all from the API
    */
      if (value.completion) {
        // Store the text from the editor
        editorText.current = text;
        // Store the completion from the API
        autoComplete.current = value.completion.trim();
        // innerHTML is <p> content here </p>
        // Get the index of the last </p> tag
        var n = val.lastIndexOf("</p>");
        // Replace the last </p> tag with the completion
        var str2 =
          val.substring(0, n) +
          `<span style="color: rgba(117, 117, 117, 0.3);" data-attr="sdsd">${value.completion.trim()}</span>` +
          val.substring(n);

        console.log(
          document.querySelector(".ql-editor")?.innerHTML,
          "innerhtml"
        );
        // Paste the HTML into the editor
        quillRef.current.editor.clipboard.dangerouslyPasteHTML(str2, "api");
        // Set the selection to the end of the current text
        quillRef.current.editor.setSelection(text.length);
        // Set the key stroke to false
        keyStroke.current = false;
      }
    }
  };

  const handleSave = () => {
    if (
      prevValues.current.title !== title ||
      prevValues.current.content !==
        document.querySelector(".ql-editor")?.innerHTML
    ) {
    }

    if (autoComplete.current === "" && title) {
      setIsSaving(true);
      axios
        .put(
          `${import.meta.env.VITE_BASE_API}/save`,
          {
            title,
            body: document.querySelector(".ql-editor")?.innerHTML,
            date: new Date().getTime(),
            doc_id: docId,
          },
          {
            headers: {
              Authorization: `Bearer ${window.localStorage.getItem("userId")}`,
            },
          }
        )
        .then((res) => {
          setIsSaving(false);
          console.log(res, "RESSSS");
          prevValues.current.title = title;
          // @ts-ignore
          prevValues.current.content =
            document.querySelector(".ql-editor")?.innerHTML;
        });
    }
  };

  const debounceHandleFetch = _.debounce(handleFetch, 1000);
  const debounceSave = _.debounce(handleSave, 4000);
  const handleChange = (val: string) => {
    if (signalRef.current) {
      signalRef.current.abort();
    }
    debounceHandleFetch(val);
    debounceSave();
  };

  useEffect(() => {
    debounceSave();
  }, [title]);

  console.log(
    editorText,
    quillRef.current,
    document.querySelector(".ql-editor")?.innerHTML
  );

  const processName = (isSaving: boolean, isFetching: boolean): string => {
    if (isSaving) {
      return "Saving...";
    }
    if (isFetching) {
      return "Fetching...";
    }
    return "";
  };

  return (
    <>
      <section className="p-8">
        <div className="max-w-3xl mx-auto mb-4">
          <div
            className={`flex items-center ${
              isSaving || isFetching ? "" : "opacity-0"
            }`}
          >
            <SavingLoader className="animate-spin origin-center text-gray-400">
              <SymbolIcon />
            </SavingLoader>
            <p className="ml-2 text-xs text-gray-400">
              {processName(isSaving, isFetching)}
            </p>
          </div>

          <div className="flex justify-between">
            <LabelRoot htmlFor="email">Title</LabelRoot>
            <FeebBackForm />
          </div>
          <TitleInput
            placeholder="New Title here...."
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
            }}
          />
        </div>
        <div className="App max-w-3xl flex flex-col mx-auto my-0 rounded-lg bg-white">
          <label className="multi-suggestion flex items-center mt-1"></label>
          <ReactQuill
            placeholder="start writing something..."
            className="w-full quill-container"
            onChangeSelection={(e: any) => {
              if (
                autoComplete.current &&
                e.index >= editorText.current.length
              ) {
                quillRef.current.editor.setSelection(editorText.current.length);
              }
            }}
            modules={{
              toolbar: tools,
              history: {
                userOnly: true,
              },
            }}
            ref={quillRef}
            onChange={handleChange}
            defaultValue={editorText.current}
          />
        </div>
      </section>

      <footer className="flex justify-center sticky mt-4">
        2023 @ scrible
      </footer>
    </>
  );
}

export default App;
