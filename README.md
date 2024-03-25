# Cinema
<p>Movie ticket sales site based on Django Rest Framework or DRF .</p>
<p>This site is for the cinema to manage the tickets of each movie .</p>
<h3>Image Database for based Postgresql in Project </h3>

![image database](https://github.com/AliReza7222/Cinema/blob/main/image_database/drawSQL-cinema-project-export-2023-08-28%20(1).png)

<hr>
<h3>SingUp</h3>
<p>To enter an important place on the site, you must log in first. Therefore, to register, the user must enter a phone number that is not currently registered.</p>

<h3>SingIn</h3>
<p>To log in, you must enter the phone number that you registered before. If the number is valid, a confirmation code will be sent to your phone number, and if you enter a valid code, you will enter the site.</p>

> <p>Authentication is based on jwt token .</p>

<h3>Payment Simulator IdPay</h3>
View TransactionsView is for buy ticket movie , after pay amount movie a ticket with key data create for client user .
<p>superuser can check data tickt movie with view DecodeDataTicket .</p>

<h3>ShowAllMovie and </h3>
<p>any user can see movie's information and don't need to login in site !</p>

<h3>Views RecordRoomView and RecordMovieView</h3>
<p>With These views superuser can create movie and room in database .</p>
