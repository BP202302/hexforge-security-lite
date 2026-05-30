package com.example.restaurantapp

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.restaurantapp.databinding.ActivityMainBinding
import com.google.firebase.auth.FirebaseAuth

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        auth = FirebaseAuth.getInstance()

        setupUI()
        checkCurrentUser()
    }

    private fun setupUI() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.title = getString(R.string.app_name)

        binding.botonRestaurantes.setOnClickListener {
            showComingSoon(getString(R.string.restaurants))
        }

        binding.botonPromociones.setOnClickListener {
            showComingSoon(getString(R.string.promotions))
        }

        binding.botonReservas.setOnClickListener {
            showComingSoon(getString(R.string.reservations))
        }

        binding.botonPerfil.setOnClickListener {
            showComingSoon(getString(R.string.profile))
        }

        binding.botonCarrito.setOnClickListener {
            showComingSoon(getString(R.string.cart))
        }
    }

    private fun checkCurrentUser() {
        val currentUser = auth.currentUser

        if (currentUser == null) {
            goToLogin()
            return
        }

        val email = currentUser.email.orEmpty()
        val nombre = currentUser.displayName
            ?.takeIf { it.isNotBlank() }
            ?: email.substringBefore("@").takeIf { it.isNotBlank() }
            ?: "Usuario"

        binding.textoBienvenida.text = "${getString(R.string.welcome)}, $nombre"
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_logout -> {
                logout()
                true
            }

            R.id.action_settings -> {
                showComingSoon(getString(R.string.settings))
                true
            }

            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun logout() {
        auth.signOut()
        goToLogin()
    }

    private fun goToLogin() {
        val intent = Intent(this, LoginActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        startActivity(intent)
        finish()
    }

    private fun showComingSoon(featureName: String) {
        Toast.makeText(
            this,
            "$featureName estará disponible próximamente",
            Toast.LENGTH_SHORT
        ).show()
    }
}
