def get_recommendations(prediction):

    if prediction == "Autism Detected":

        return {

            "status": "High Possibility of Autism Spectrum Disorder",

            "recommendations": [

                "Consult a pediatric neurologist or developmental pediatrician.",

                "Schedule a comprehensive Autism Spectrum Disorder (ASD) evaluation.",

                "Begin early intervention programs if recommended by a specialist.",

                "Consider Speech and Language Therapy.",

                "Consider Occupational Therapy to improve daily living skills.",

                "Behavioral Therapy (ABA) may help improve communication and social interaction.",

                "Maintain a structured daily routine for your child.",

                "Encourage eye contact, communication, and interactive play.",

                "Monitor developmental milestones regularly.",

                "Provide emotional support and positive reinforcement."

            ]

        }

    else:

        return {

            "status": "Low Possibility of Autism Spectrum Disorder",

            "recommendations": [

                "Continue monitoring your child's developmental milestones.",

                "Encourage social interaction with family members and peers.",

                "Read books and communicate with your child regularly.",

                "Promote healthy eating and adequate sleep.",

                "Encourage outdoor activities and physical exercise.",

                "Attend routine pediatric health check-ups.",

                "If developmental concerns arise, consult a healthcare professional."

            ]

        }