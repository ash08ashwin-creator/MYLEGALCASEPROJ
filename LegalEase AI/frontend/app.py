import requests
import streamlit as st

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Drafting")

st.info(
    "Enter the required information below to generate a draft legal document. "
    "The generated document should be reviewed by a qualified legal professional "
    "before use."
)

document_type = st.text_input(
    "Document Type",
    value="Rental Agreement"
)

parties = st.text_area(
    "Parties",
    value="Landlord: John Smith; Tenant: Rahul Kumar"
)

terms = st.text_area(
    "Terms",
    value=(
        "Monthly rent is ₹15,000. Security deposit is ₹30,000. "
        "The tenancy period is 11 months. "
        "The tenant must pay rent on or before the 5th day of each month."
    )
)

dates = st.text_area(
    "Dates",
    value="Agreement starts on 1 October 2026 and ends on 31 August 2027."
)

jurisdiction = st.text_input(
    "Jurisdiction",
    value="Tamil Nadu, India"
)

additional_instructions = st.text_area(
    "Additional Instructions",
    value=(
        "Generate a clear, structured rental agreement "
        "with headings and numbered clauses."
    )
)

if st.button("Generate Document", type="primary"):

    if not document_type or not parties or not terms:
        st.error(
            "Please fill in Document Type, Parties, and Terms."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
            "jurisdiction": jurisdiction,
            "additional_instructions": additional_instructions,
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=payload,
                    timeout=120,
                )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Document generated successfully!"
                )

                st.markdown("## Generated Document")

                st.markdown(
                    result["content"]
                )

                st.download_button(
                    label="Download Document",
                    data=result["content"],
                    file_name="legal_document.md",
                    mime="text/markdown",
                )

            else:

                try:
                    error = response.json()
                except Exception:
                    error = response.text

                st.error(
                    f"Backend returned HTTP "
                    f"{response.status_code}: {error}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the LegalEase backend. "
                "Please start the FastAPI server first."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. "
                "The AI service may be busy. "
                "Please try again."
            )

        except Exception as exc:

            st.error(
                f"Unexpected error: {exc}"
            )
