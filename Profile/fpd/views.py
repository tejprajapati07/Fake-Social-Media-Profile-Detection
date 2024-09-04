from django.shortcuts import render, HttpResponse, redirect
import numpy as np
import pandas as pd
import tensorflow as tf
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm
from .forms import ContactForm
from .models import Contact
# from django.contrib.auth import authenticate


# Load the model using TFSMLayer
model = tf.keras.models.load_model('static\static\model_ANN.h5')



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, "about.html")


# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return redirect('success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


def success_view(request):
    return HttpResponse("Thank you for contacting us!")

def learnmore(request):
    return render(request, 'learnmore.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        # Check if the form's error message contains an error related to authentication
        if 'username' in form.errors or 'password' in form.errors:
            # If either the username or password is invalid, display a specific error message
            messages.error(self.request, "Incorrect username or password.")
        else:
            # If the password is incorrect (but username is valid), display the default message
            return super().form_invalid(form)
        # Add error messages to the context
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
 


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Login to continue.')
            return redirect('login')  # Redirect to the login page
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def prediction(request):
    if request.method == "POST":
        profile_pic = int(request.POST.get('profile_pic'))
        nums_length_username = float(request.POST.get('nums/length_username'))
        fullname_words = int(request.POST.get('fullname_words'))
        nums_length_fullname = float(request.POST.get('nums/length_fullname'))
        name__username = int(request.POST.get('name==username'))
        description_length = int(request.POST.get('description_length'))
        external_URL = int(request.POST.get('external_URL'))
        private = int(request.POST.get('private'))
        posts = int(request.POST.get('posts'))
        followers = int(request.POST.get('followers'))
        follows = int(request.POST.get('follows'))

        data = {
            'profile pic':profile_pic,
            'nums/length username':nums_length_username,
            'fullname words':fullname_words,
            'nums/length fullname':nums_length_fullname,
            'name==username':name__username,	
            'description length':description_length,
            'external URL':external_URL,	
            'private':private,
            '#posts':posts,	
            '#followers':followers,	
            '#follows':follows,
        }

        from sklearn.preprocessing import StandardScaler

        scaler_x = StandardScaler()
        new_df = pd.DataFrame(data, index=[0])
        print(new_df)
        instagram_df_train=pd.read_csv('static\insta_train.csv')
        X_train = instagram_df_train.drop(columns = ['fake'])
        # pred = model.predict(new_df)
        scaler_x.fit_transform(X_train)
        scaled_new_data = scaler_x.transform(new_df) 
        # Scale the new data using the same scaler used for training data
        # Predicting using the trained model
        predicted_new_data = model.predict(scaled_new_data)
        print(predicted_new_data)
        # Interpret the prediction
        predicted_label = np.argmax(predicted_new_data)  
        print(predicted_label)
        # Get the index of the predicted class
        if predicted_label == 0:
            pred = "The profile is predicted to be real."
        else:
            pred = "The profile is predicted to be fake."
        print(pred)
        output = {
            "output": pred
            }
        return render(request, 'prediction.html', output)

    else:
        return render(request, 'prediction.html')