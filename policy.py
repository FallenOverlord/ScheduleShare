import streamlit as st

def user_agreement():

    # Expandable user policy agreement
    with st.expander("User Policy Agreement"):
        st.markdown("""
        ### User Information Security Policy
        **1. Data Protection**
        - We implement robust security measures to protect user data from unauthorized access, alteration, disclosure, or destruction.
        - All sensitive information, such as passwords, is encrypted using industry-standard encryption protocols.

        **2. Data Usage**
        - User data is collected solely for the purpose of providing and improving our services.
        - We do not share personal information with third parties without user consent, except as required by law.

        **3. User Rights**
        - Users have the right to access, correct, or delete their personal data.
        - Users can request to view their data and update it through their profile settings.

        ### User Policy
        **1. Account Responsibility**
        - Users are responsible for maintaining the confidentiality of their account credentials.
        - Users must notify us immediately of any unauthorized use of their account.

        **2. Acceptable Use**
        - Users must not use the service for any unlawful or prohibited activities.
        - Users must respect the rights of others and not engage in harassment, discrimination, or any harmful behavior.

        ### Terms of Service
        **1. Service Availability**
        - We strive to ensure the continuous availability of our service, but we do not guarantee uninterrupted access.
        - We reserve the right to suspend or terminate accounts for violations of our policies.

        **2. Changes to Terms**
        - We may update these terms from time to time. Users will be notified of any significant changes.
        - Continued use of the service constitutes acceptance of the new terms.

        **3. Limitation of Liability**
        - We are not liable for any indirect, incidental, or consequential damages arising from the use of our service.
        - Our total liability is limited to the amount paid by the user for the service, if applicable.
        """)

        accept_policy = st.checkbox("I accept the user policy agreement")

        return accept_policy