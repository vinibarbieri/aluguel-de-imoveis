import { useEffect, useState } from "react";
import axios from "axios";
import { getLoggedUser, logout } from "../utils/auth";
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';


interface Property {
  id: number;
  title: string;
  description: string;
  address: string;
  price_per_day: number;
  available_from: string;
  available_until: string;
  image_url?: string;
  total_reservas?: number;
  average_rating?: number;
}

interface Reservation {
    reservation_id: number;
    property_id: number;
    renter_name: string;
    start_date: string;
    end_date: string;
    approved: boolean | null;
  }
  
export default function LocadorDashboard() {
  const user = getLoggedUser();
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [tab, setTab] = useState<"list" | "create" | "reservas">("list");
  const [properties, setProperties] = useState<Property[]>([]);
  const [form, setForm] = useState({
    id: null,
    title: "",
    description: "",
    address: "",
    price_per_day: "",
    available_from: "",
    available_until: "",
    image_url: "",
    average_rating: null,
  });

  const loadProperties = async () => {
    const res = await axios.get(`http://localhost:5000/api/locador/properties/${user.id}`);
    setProperties(res.data);
  };

  const loadReservations = async () => {
    const res = await axios.get(`http://localhost:5000/api/locador/reservations/${user.id}`);
    setReservations(res.data);
  };

  useEffect(() => {
    loadProperties();
    loadReservations();
  }, []);

  const handleCreate = async () => {
    try {
      const data = {
        ...form,
        price_per_day: parseFloat(form.price_per_day),
        owner_id: user.id,
      };
  
      if (form.id) {
        await axios.put(`http://localhost:5000/api/locador/property/${form.id}`, data);
        alert("Imóvel atualizado!");
      } else {
        await axios.post("http://localhost:5000/api/locador/properties", data);
        alert("Imóvel cadastrado!");
      }
  
      resetForm();
      setTab("list");
      loadProperties();
    } catch (err) {
      alert("Erro ao salvar imóvel.");
    }
  };
  
  const resetForm = () =>
    setForm({
      id: null,
      title: "",
      description: "",
      address: "",
      price_per_day: "",
      available_from: "",
      available_until: "",
      image_url: "",
    });

    const handleEdit = (p: any) => {
        setForm({
          id: p.id,
          title: p.title,
          description: p.description,
          address: p.address,
          price_per_day: p.price_per_day.toString(),
          available_from: p.available_from,
          available_until: p.available_until,
          image_url: p.image_url || "",
        });
        setTab("create");
      };
      
    const handleDelete = async (id: number) => {
        if (!confirm("Tem certeza que deseja excluir este imóvel?")) return;
        
        try {
            await axios.delete(`http://localhost:5000/api/locador/property/${id}`);
            alert("Imóvel removido!");
            loadProperties();
        } catch (err) {
            alert("Erro ao excluir imóvel.");
        }
    };
      
  

  const handleUpdateReservation = async (id: number, approved: boolean) => {
    try {
      await axios.put(`http://localhost:5000/api/locador/reservation/${id}`, { approved });
      alert("Reserva atualizada!");
      loadReservations();
    } catch (err) {
      alert("Erro ao atualizar reserva");
    }
  };
  

  return (
    <div className="container mt-4">
      <h2>Olá, {user.name}</h2>
      <button className="btn btn-outline-danger float-end" onClick={logout}>
        Sair
      </button>

      <ul className="nav nav-tabs mt-4">
        <li className="nav-item">
          <button className={`nav-link ${tab === "list" ? "active" : ""}`} onClick={() => setTab("list")}>
            Meus Imóveis
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${tab === "create" ? "active" : ""}`} onClick={() => setTab("create")}>
            Cadastrar Novo
          </button>
        </li>
        <li className="nav-item">
            <button className={`nav-link ${tab === "reservas" ? "active" : ""}`} onClick={() => setTab("reservas")}>
                Reservas Recebidas
            </button>
        </li>
      </ul>

      <div className="mt-4">
        {tab === "list" && (
          <div>
            <h4>Imóveis Cadastrados</h4>
            {properties.map((p) => (
                <div key={p.id} className="card mb-3">
                    {p.image_url && (
                    <img
                        src={p.image_url}
                        alt={p.title}
                        className="card-img-top"
                        style={{ maxHeight: "300px", objectFit: "cover" }}
                    />
                    )}
                    <div className="card-body">
                    <h5 className="card-title">{p.title}</h5>
                    <p>{p.description}</p>
                    <p className="text-muted">{p.address}</p>
                    <p>
                        💵 R${p.price_per_day} | Disponível de {p.available_from} até {p.available_until}
                    </p>
                    <p>📅 {p.total_reservas ?? 0} reservas | ⭐ {p.average_rating ?? "sem avaliação"}</p>
                    <button className="btn btn-warning me-2" onClick={() => handleEdit(p)}>Editar</button>
                    <button className="btn btn-danger" onClick={() => handleDelete(p.id)}>Excluir</button>
                    </div>
                </div>
                ))}

          </div>
        )}

        {tab === "create" && (
          <div>
            <h4>Cadastrar Novo Imóvel</h4>
            <input className="form-control mb-2" placeholder="Título" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            <textarea className="form-control mb-2" placeholder="Descrição" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            <GooglePlacesAutocomplete
                apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
                selectProps={{
                    placeholder: 'Buscar endereço...',
                    onChange: (value: any) => {
                    setForm({ ...form, address: value.label });
                    },
                    styles: {
                    control: (base) => ({
                        ...base,
                        marginBottom: '0.5rem'
                    })
                    }
                }}
            />       
            {form.address && (
                <input
                    className="form-control mb-2"
                    value={form.address}
                    disabled
                />
            )}
            <input type="number" className="form-control mb-2" placeholder="Valor da diária" value={form.price_per_day} onChange={(e) => setForm({ ...form, price_per_day: e.target.value })} />
            <input type="date" className="form-control mb-2" value={form.available_from} onChange={(e) => setForm({ ...form, available_from: e.target.value })} />
            <input type="date" className="form-control mb-2" value={form.available_until} onChange={(e) => setForm({ ...form, available_until: e.target.value })} />
            <input
                className="form-control mb-2"
                placeholder="URL da imagem do imóvel"
                value={form.image_url}
                onChange={(e) => setForm({ ...form, image_url: e.target.value })}
            />

            <button className="btn btn-success" onClick={handleCreate}>
              Cadastrar
            </button>
          </div>
        )}

        {tab === "reservas" && (
            <div>
                <h4>Reservas Recebidas</h4>
                {reservations.length === 0 && <p>Nenhuma reserva ainda.</p>}
                {reservations.map((r) => (
                    <div key={r.reservation_id} className="card mb-3">
                        <div className="card-body">
                            <p><strong>Imóvel ID:</strong> {r.property_id}</p>
                            <p><strong>Locatário:</strong> {r.renter_name}</p>
                            <p><strong>Período:</strong> {r.start_date} até {r.end_date}</p>
                            <p><strong>Status:</strong> {r.approved === null ? "Pendente" : r.approved ? "Aprovada" : "Recusada"}</p>
                            <p><strong>⭐</strong>{r.average_rating ?? "sem avaliação"}</p>

                            {r.approved === null && (
                                <>
                                    <button className="btn btn-success me-2" onClick={() => handleUpdateReservation(r.reservation_id, true)}>
                                        Aprovar
                                    </button>
                                    <button className="btn btn-danger" onClick={() => handleUpdateReservation(r.reservation_id, false)}>
                                        Recusar
                                    </button>
                                </>
                            )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    </div>
  );
}
