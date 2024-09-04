import React from "react";
import { FilePlusIcon, FileTextIcon, TrashIcon } from "@radix-ui/react-icons";
import { styled } from "@stitches/react";
import * as Separator from "@radix-ui/react-separator";
import * as ContextMenu from "@radix-ui/react-context-menu";
import { violet, mauve } from "@radix-ui/colors";
import { useDocuments } from "../../hooks/queries/useDocuments";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const DashboardContainer = styled("div", {
  maxWidth: "1200px",
  margin: "0 auto",
  background: "white",
  border: "1px solid #efefef",
  padding: "1rem 2rem",
});

const Heading = styled("h1", {
  letterSpacing: "-0.09em",
  fontSize: "2.6rem",
  color: "rgb(40, 42, 48)",
  // fontFamily: "'Fredoka One', cursive",
});

const Button = styled("button", {
  boxShadow: "rgb(0 0 0 / 9%) 0px 1px 1px",
  border: "1px solid rgb(223, 225, 228)",
  color: "rgb(60, 65, 73)",
  "transition-property": "border, background-color, color, box-shadow, opacity",
  "transition-duration": "0.1s",
  borderRadius: "6px",
  fontWeight: 500,
  display: "flex",
  alignItems: "center",
  gap: "8px",
  letterSpacing: "-0.04em",
  padding: "0 1rem",
  height: 40,
  "&:hover": {
    background: "rgb(244, 245, 248)",
    border: " 1px solid rgb(201, 203, 205)",
  },
});

const ListItem = styled("a", {
  height: "44px",
  display: "flex",
  alignItems: "center",
  padding: "0 1rem",
  cursor: "pointer",
  "&:hover": {
    background: "#fbfbfc",
  },
});

const ListSeprator = styled(Separator.Root, {
  background: "#eef0f3",
  height: "1px",
  width: "100%",
});

const ContextMenuContainer = ({ children, onEdit }) => {
  return (
    <ContextMenu.Root>
      <ContextMenuTrigger>{children}</ContextMenuTrigger>
      <ContextMenu.Portal>
        <ContextMenuContent sideOffset={5} align="end">
          <ContextMenuItem onClick={onEdit}>
            Edit <RightSlot>Edit doc</RightSlot>
          </ContextMenuItem>
          <ContextMenuItem>
            Delete <RightSlot>Delete doc</RightSlot>
          </ContextMenuItem>
        </ContextMenuContent>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
};

const Dashboard = () => {
  const { data, refetch } = useDocuments();
  const navigate = useNavigate();

  const editDocumentById = (docId: string) => {
    navigate(`/editor/${docId}`);
  };

  const deleteDocument = async (docId: string) => {
    const res = await axios.post(
      `${import.meta.env.VITE_BASE_API}/delete/${docId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem("userId")}`,
        },
      }
    );
    if (res.status === 200) {
      refetch();
      alert(res.data.message);
    }
  };

  return (
    <DashboardContainer>
      <div className="flex justify-between items-center ">
        <Heading>Documents</Heading>
        <Button onClick={() => navigate("/editor")}>
          <FilePlusIcon /> New Document
        </Button>
      </div>
      <div>
        {data?.map((docsData) => {
          return (
            <ContextMenuContainer
              key={docsData.doc_id}
              onEdit={() => editDocumentById(docsData.doc_id)}
            >
              <ListItem onClick={() => editDocumentById(docsData.doc_id)}>
                <div className="flex justify-between w-full items-baseline my-10 ">
                  <div className="flex items-baseline">
                    <FileTextIcon className="mr-2" />{" "}
                    <p className="m-w-36 whitespace-nowrap text-ellipsis overflow-hidden">
                      {docsData.title}
                    </p>
                    <p className="text-xs ml-2 text-gray-600 w-80 whitespace-nowrap text-ellipsis overflow-hidden">
                      <span
                        dangerouslySetInnerHTML={{ __html: docsData.body }}
                      ></span>
                    </p>
                    <span className="ml-1">...</span>
                  </div>
                  <div className="flex gap-4">
                    <p className="text-xs text-gray-500">
                      {new Date(docsData.date).toDateString()}{" "}
                    </p>

                    <TrashIcon
                      onClick={(pointerEvents) => {
                        pointerEvents.stopPropagation();
                        deleteDocument(docsData.doc_id);
                      }}
                    />
                  </div>
                </div>
              </ListItem>
            </ContextMenuContainer>
          );
        })}
        <ListSeprator />
      </div>
    </DashboardContainer>
  );
};

const ContextMenuTrigger = styled(ContextMenu.Trigger, {});

const contentStyles = {
  minWidth: 220,
  backgroundColor: "white",
  borderRadius: 6,
  overflow: "hidden",
  padding: 5,
  border: "1px solid #e6e8eb",
  // boxShadow:
  //   "0px 10px 38px -10px rgba(22, 23, 24, 0.35), 0px 10px 20px -15px rgba(22, 23, 24, 0.2)",
};

const ContextMenuContent = styled(ContextMenu.Content, contentStyles);
const ContextMenuSubContent = styled(ContextMenu.SubContent, contentStyles);

const itemStyles = {
  fontSize: 13,
  lineHeight: 1,
  color: violet.violet11,
  borderRadius: 3,
  display: "flex",
  alignItems: "center",
  height: 25,
  padding: "0 5px",
  position: "relative",
  paddingLeft: 10,
  userSelect: "none",
  outline: "none",

  "&[data-disabled]": {
    color: mauve.mauve8,
    pointerEvents: "none",
  },

  "&[data-highlighted]": {
    backgroundColor: violet.violet9,
    color: violet.violet1,
  },
};

const ContextMenuItem = styled(ContextMenu.Item, itemStyles);
const ContextMenuCheckboxItem = styled(ContextMenu.CheckboxItem, itemStyles);
const ContextMenuRadioItem = styled(ContextMenu.RadioItem, itemStyles);
const ContextMenuSubTrigger = styled(ContextMenu.SubTrigger, {
  '&[data-state="open"]': {
    backgroundColor: violet.violet4,
    color: violet.violet11,
  },
  ...itemStyles,
});

const ContextMenuLabel = styled(ContextMenu.Label, {
  paddingLeft: 25,
  fontSize: 12,
  lineHeight: "25px",
  color: mauve.mauve11,
});

const ContextMenuSeparator = styled(ContextMenu.Separator, {
  height: 1,
  backgroundColor: violet.violet6,
  margin: 5,
});

const ContextMenuItemIndicator = styled(ContextMenu.ItemIndicator, {
  position: "absolute",
  left: 0,
  width: 25,
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
});

const RightSlot = styled("div", {
  marginLeft: "auto",
  paddingLeft: 20,
  fontSize: 12,
  color: mauve.mauve11,
  "[data-highlighted] > &": { color: "white" },
  "[data-disabled] &": { color: mauve.mauve8 },
});

export default Dashboard;
