import streamlit as st
import os

def navigate(course, university, level, rate, description, spec, skills, img):
    # store in session
    st.session_state.landing_page_params = {
        "course": course,
        "level": level,
        "rate": rate,
        "description": description,
        "spec": spec,
        "university": university,
        "skills": skills,
        "img": img
    }
    
    # create url with params
    port = os.environ.get("PORT", "8501")
    url = f"http://localhost:{port}/landingpage?"
    url += f"course={course}&"
    url += f"level={level}&"
    url += f"rate={rate}&"
    url += f"description={description}&"
    url += f"spec={spec}&"
    url += f"university={university}&"
    url += f"skills={skills}&"
    url += f"img={img}"
    
    # Navigate to new url
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}" />', unsafe_allow_html=True)
    
    # update query prams
    query_params = st.experimental_get_query_params()
    st.experimental_set_query_params(
        page="landingpage",
        course=course,
        level=level,
        rate=rate,
        description=description,
        spec=spec,
        university=university,
        img=img
    )

    if "page" in query_params and query_params["page"][0] == "landingpage":
        # if landingexit --> navigate to landingpage
        import pages.landingpage 
        pages.landingpage  # execute command in landingpage
        st.stop()  
    st.experimental_rerun()